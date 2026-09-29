# ClassTrack

#### Video Demo: https://drive.google.com/file/d/189g-2ismLJE5E5ZaO1uGuQDBhvDizPqi/view?usp=drivesdk

#### Description:

ClassTrack is a web-based Student Management System designed to help teachers manage student information, attendance, and grades in one organized application. The main purpose of the project is to provide a simple and organized way for teachers to keep track of their students instead of managing this information manually or using different files.

The application was built using Python, Flask, HTML, CSS, and SQLite. Python is the main programming language used in the project, while Flask is the web framework that connects the backend logic with the web pages. HTML is used to create the structure and content of the pages, CSS is used to control their appearance, and SQLite is used to store the application's data.

The main file in the project is `app.py`. This file contains the Flask application and the main routes used by ClassTrack. It is responsible for starting the web application and handling the requests made by the user. It also connects the application to the SQLite database and contains the logic for managing students, attendance, grades, reports, and statistics.

The application creates and uses a SQLite database called `students.db`. This database is responsible for storing the information used by the system. It stores student information, attendance records, and grades. Using a database is important because the information needs to remain available after the application is closed or restarted.

The `templates` folder contains the HTML pages used by the application. The `layout.html` file provides the common structure used across the website. Other template files are responsible for different pages and features of the system, including the students page, adding students, editing students, attendance, grades, reports, and statistics. Using separate templates makes the project more organized and makes each part of the website easier to maintain.

The `static` folder contains the `style.css` file. This file is responsible for the visual design of the application. It controls the layout, spacing, buttons, tables, forms, fonts, and other visual elements. I used CSS to make the website easier to read and more organized for the teacher using the system.

One of the main features of ClassTrack is student management. The teacher can add a new student to the system, and the student is assigned a unique code. This code can then be used to identify the student. The teacher can also edit existing student information or delete a student when necessary. A search feature is also included so that the teacher can find a student by name.

The attendance feature allows the teacher to record attendance for students during different lectures. The teacher can select a lecture and record whether each student was present or absent. These attendance records are stored in the database and can later be used to calculate the student's attendance percentage.

The grades feature allows the teacher to record different types of assessments. The system supports Quiz, Assignment, Midterm, and Final grades. The teacher can enter the grade for a student and the information is saved in the database. This makes it possible to keep academic information organized in the same system as the attendance records.

ClassTrack also includes a student report feature. The report provides information about an individual student, including the student's name and code, attendance information, attendance percentage, and grades. This gives the teacher a quick overview of the student's performance without having to manually calculate the information.

Another feature is the statistics page. It provides general information about the class, such as the total number of students, average attendance, and average grades. This can help the teacher get a quick overview of the class performance.

I chose Flask because I wanted to build a real web application while continuing to us


## Deployment

This project can be deployed as a Flask web service using Gunicorn. For Render, use `pip install -r requirements.txt` as the build command and `gunicorn app:app` as the start command.
