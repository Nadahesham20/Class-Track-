from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


# Create database
db = get_db()

db.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        lecture INTEGER NOT NULL,
        present INTEGER NOT NULL DEFAULT 0
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        assessment TEXT NOT NULL,
        grade REAL NOT NULL
    )
""")

db.commit()
db.close()


# Home page
@app.route("/")
def index():

    db = get_db()

    students = db.execute("""
        SELECT * FROM students
        ORDER BY id
    """).fetchall()

    db.close()

    return render_template("index.html", students=students)


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]

        db = get_db()

        db.execute(
            "INSERT INTO students (name) VALUES (?)",
            (name,)
        )

        db.commit()
        db.close()

        return redirect("/")

    return render_template("add_student.html")


# Edit student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    db = get_db()

    student = db.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]

        db.execute(
            "UPDATE students SET name = ? WHERE id = ?",
            (name, id)
        )

        db.commit()
        db.close()

        return redirect("/")

    db.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):

    db = get_db()

    db.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    db.execute(
        "DELETE FROM attendance WHERE student_id = ?",
        (id,)
    )

    db.execute(
        "DELETE FROM grades WHERE student_id = ?",
        (id,)
    )

    db.commit()
    db.close()

    return redirect("/")


# Search
@app.route("/search")
def search():

    query = request.args.get("q", "")

    db = get_db()

    students = db.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        ORDER BY id
    """, ("%" + query + "%",)).fetchall()

    db.close()

    return render_template(
        "index.html",
        students=students,
        search=query
    )


# Attendance
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    db = get_db()

    students = db.execute("""
        SELECT * FROM students
        ORDER BY id
    """).fetchall()

    if request.method == "POST":

        lecture = int(request.form["lecture"])

        for student in students:

            value = request.form.get(
                f"student_{student['id']}"
            )

            present = 1 if value == "present" else 0

            old = db.execute("""
                SELECT id FROM attendance
                WHERE student_id = ? AND lecture = ?
            """, (student["id"], lecture)).fetchone()

            if old:

                db.execute("""
                    UPDATE attendance
                    SET present = ?
                    WHERE student_id = ? AND lecture = ?
                """, (
                    present,
                    student["id"],
                    lecture
                ))

            else:

                db.execute("""
                    INSERT INTO attendance
                    (student_id, lecture, present)
                    VALUES (?, ?, ?)
                """, (
                    student["id"],
                    lecture,
                    present
                ))

        db.commit()
        db.close()

        return redirect("/attendance")

    db.close()

    return render_template(
        "attendance.html",
        students=students
    )


# Grades
@app.route("/grades", methods=["GET", "POST"])
def grades():

    db = get_db()

    students = db.execute("""
        SELECT * FROM students
        ORDER BY id
    """).fetchall()

    if request.method == "POST":

        student_id = int(request.form["student_id"])
        assessment = request.form["assessment"]
        grade = float(request.form["grade"])

        db.execute("""
            INSERT INTO grades
            (student_id, assessment, grade)
            VALUES (?, ?, ?)
        """, (
            student_id,
            assessment,
            grade
        ))

        db.commit()
        db.close()

        return redirect("/grades")

    all_grades = db.execute("""
        SELECT
            grades.id,
            students.name,
            grades.student_id,
            grades.assessment,
            grades.grade
        FROM grades
        JOIN students
        ON students.id = grades.student_id
        ORDER BY grades.id DESC
    """).fetchall()

    db.close()

    return render_template(
        "grades.html",
        students=students,
        grades=all_grades
    )


# Student report
@app.route("/report/<int:id>")
def report(id):

    db = get_db()

    student = db.execute("""
        SELECT * FROM students
        WHERE id = ?
    """, (id,)).fetchone()

    grades = db.execute("""
        SELECT * FROM grades
        WHERE student_id = ?
    """, (id,)).fetchall()

    attendance = db.execute("""
        SELECT * FROM attendance
        WHERE student_id = ?
    """, (id,)).fetchall()

    db.close()

    total_lectures = len(attendance)

    present = sum(
        row["present"] for row in attendance
    )

    if total_lectures > 0:
        attendance_percentage = (
            present / total_lectures
        ) * 100
    else:
        attendance_percentage = 0

    if len(grades) > 0:
        average_grade = sum(
            row["grade"] for row in grades
        ) / len(grades)
    else:
        average_grade = 0

    return render_template(
        "report.html",
        student=student,
        grades=grades,
        total_lectures=total_lectures,
        present=present,
        attendance_percentage=attendance_percentage,
        average_grade=average_grade
    )


# Statistics
@app.route("/statistics")
def statistics():

    db = get_db()

    students = db.execute("""
        SELECT * FROM students
    """).fetchall()

    total_students = len(students)

    total_attendance = db.execute("""
        SELECT SUM(present) AS total
        FROM attendance
    """).fetchone()["total"]

    total_records = db.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
    """).fetchone()["total"]

    if total_records > 0:
        average_attendance = (
            total_attendance / total_records
        ) * 100
    else:
        average_attendance = 0

    average_grade = db.execute("""
        SELECT AVG(grade) AS average
        FROM grades
    """).fetchone()["average"]

    if average_grade is None:
        average_grade = 0

    db.close()

    return render_template(
        "statistics.html",
        total_students=total_students,
        average_attendance=average_attendance,
        average_grade=average_grade
    )


if __name__ == "__main__":
    app.run(debug=True)
