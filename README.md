# CRUD Web Application For Student Database Management System
#### Video Demo:  https://www.youtube.com/watch?v=qPDPRf1rpRI
#### Description:

# CRUD Web Application For Student Database Management System

This Python-based web application, leveraging Flask, SQLite, and Bootstrap, empowers users to securely manage student records through a sophisticated user interface. The application seamlessly integrates CRUD (Create, Read, Update, Delete) functionalities, including recent enhancements using JavaScript, into a robust system for efficient database management.

## Features

### User Authentication

- **Register:** Users can create an account by providing a unique username and a securely hashed password. The application employs Flask's `generate_password_hash` function to enhance password security.

- **Login:** Existing users can log in using their credentials, with the system performing rigorous checks on both the hashed password and the username for a comprehensive verification process.

- **Logout:** Users can securely log out of their accounts, ensuring a smooth and protected end to their session.

### Student Database Operations

- **Add Student Record:** Each user is assigned a unique ID, facilitating association with specific records. Users can seamlessly add new student records, inputting relevant data such as the student's name, city, and contact number.

- **View Student Records:** The main page showcases a comprehensive table of student records, including ID, name, city, and contact number, for convenient and organized data access.

- **Edit Student Record:** To uphold data security standards, users can exclusively edit the records they have entered. The application ensures user data privacy by permitting edits only on records associated with the user's unique session ID.

- **Delete Student Record:** Users can delete their inputted data, with the application verifying the user's ID for deletion authorization, reinforcing data privacy measures.

### Export Data

- **Export as CSV:** The export section is implemented with JavaScript to ensure heightened data security. Users can export only their specific data associated with the session ID from which they are logged in. This implementation restricts the export functionality to provide users with exclusive access to their data, reinforcing the overall integrity and privacy of the application.

The application diligently stores inputted data in the 'students.db' data server, employing a secure and professional approach to safeguard user information.

