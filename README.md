# 🩸 Blood Net - Blood Donor Management System

Blood Net is a web-based Blood Donor Management System developed using Django and MySQL. The project is designed to simplify donor record management by providing an efficient way to add, view, update, and delete donor information.

This project was built as part of my learning journey in web development, where I applied the concepts I learned through tutorials, documentation, and hands-on practice to create a functional application from scratch.

## Current Features

* Register new blood donors
* View donor records
* Update donor information
* Delete donor records
* MySQL database integration
* User-friendly interface

## Future Enhancements

* User Authentication and Authorization
* Role-Based Access Control
* Advanced Search and Filtering
* Blood Availability Dashboard
* Deployment to a Live Server
* Additional validations and security improvements

## Technologies Used

* Python
* Django
* MySQL
* HTML
* CSS
* Bootstrap
* Git & GitHub

## What I Learned

Developing Blood Net helped me gain practical experience in:

* Django Models and ORM
* Forms and Validation
* CRUD Operations
* URL Routing
* Database Management
* Frontend and Backend Integration
* Version Control with Git and GitHub

## Project Status

🚧 This project is currently under active development. New features, improvements, and optimizations will be added in future updates.

## Developer

Mohamed Thawfiq

Final Year Computer Science Student | Aspiring Software Developer

## Feedback

I am continuously learning and improving my development skills. Feedback, suggestions, and contributions are always appreciated.

## Deployment

To deploy this project to Render:
1. Fix `Procfile` to `web: gunicorn tntj_bw.wsgi`
2. Push the code to GitHub under your repo.
3. Create a Render Web Service using the GitHub repository.
4. Set environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
5. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`.

You can use `.env.example` as a template for local development.
