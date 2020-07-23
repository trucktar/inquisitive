# Quiz_app

A RESTful API for a Quiz App service using Django Rest Framework.

> frontend - [visit](https://github.com/muturi254/Quiz_app_fronten)

> Android - [visit](https://github.com/muturi254/Quiz_app_Android)

## Getting Started

These instructions will get you a copy of this project up and running for local development and testing purposes.

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [Pipenv](https://github.com/pypa/pipenv#installation)
- [Git](https://git-scm.com/downloads)
- [PostgreSQL](https://www.postgresql.org/download/)

### Setup and Installation

1. Clone this [repository](https://github.com/muturi254/Quiz_app.git) using `git clone`. Then, change your working directory to the repository.

   ```
   $ git clone https://github.com/muturi254/Quiz_app.git
   $ cd Quiz_app/
   ```

2. Install project and development dependencies.

   ```
   $ pipenv sync
   ```

3. Activate the project's virtualenv

   ```
   $ pipenv shell
   ```

### Database Configuration

Ensure you have PostgreSQL installed and running. Then,

1. Enter psql, a terminal-based front-end to PostgreSQL:

   ```
   $ psql -U postgres
   ```

2. Run the following queries to create the role and database.

   ```
   postgres=# CREATE USER {{ roleName }} WITH CREATEDB;
   postgres=# CREATE DATABASE {{ dbName }} OWNER {{ roleName }};
   ```

### Launching the service

1. Create a `.env` file and set the following env variables:

   ```
   DATABASE_URL=postgres://{{ roleName }}@localhost/{{ dbName }}
   SECRET_KEY=suitable-for-development-only
   ```

2. Run the following commands to create the database tables:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a superuser account.

   ```
   python manage.py createsuperuser
   ```

4. Finally, fire up the server and navigate to http://127.0.0.1:8000/
   ```
   python manage.py runserver
   ```

## Built using

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
- [Django REST Framework](https://www.django-rest-framework.org/) - Web APIs for Django.

## Credits

[Nyota Mwangi](https://github.com/trucktar/), [Jorim Midumbi Okong'o Opondo](https://github.com/JORIM1981)

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
