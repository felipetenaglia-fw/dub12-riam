You are building a LMS (learning management system) for the RIAM (Royal Irish Academy of Music).


The RIAM came up with a framework of what makes a great musician. It is divided in 4 categories:
- Technical skill and competence
- Compositional and musicianship knowledge
- Repertoire and Cultural knowledge
- Performing Artistrty.

The application can have 3 different user roles:
- Student
- Teacher
- Admin

Students attend in-person classes with Teachers. At the end of each claass, teachers are required to write notes for the student. Notes should capture points for improvement and actions for the student to practice.

Student can be assigned tasks, such as practicing and listening to recommended music pieces. Those are teatcher's decision. After performing the tasks, students should input their feedback, like how they felt during the practice. Practice can also be recorded via the platform, and is made available to the teacher. When teachers assign musical pieces from composers, like Mozart, the student should listen and answer a quiz on selected aspects , like how they describe harmony, performance, and so on. These are available for the teacher to review.

Teachers can view the performance of their students, and assign tasks. Admins can view performance of all students, by teacher.

For now, we can have mock credentials, such as student/student, teacher/teacher, admin/admin. You can create a role for users, and define what they can do based on that.


I want you to build a python backend API, using AWS ECS, and infrastructure as code, so we can run a CDK command line and get it deployed.
To start, the app can use a SQLLite in-memory DB. I don't want to enforce physical foreign keys, let's ensure consistency in the code. Build a postman collection for consuming the API.

