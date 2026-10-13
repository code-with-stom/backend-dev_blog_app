# Encore Hub

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14.2-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.135.3-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
  <strong>A secure, developer-focused blog backend built with FastAPI and PostgreSQL.</strong>
</p>

<p align="center">
  <a href="#about-the-project">About</a> •
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#project-structure">Structure</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#api-documentation">API Documentation</a> •
  <a href="#security-considerations">Security</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## About the Project

**Encore Hub** is a developer-focused platform designed to bring developers together to share articles, exchange knowledge, and make technical information more accessible to the public.

The project provides a backend for a blog website, with a focus on authentication, database management, and a structured API architecture.

It was built to demonstrate practical experience with:

* REST API development using FastAPI.
* JWT-based authentication.
* Password hashing and user security.
* PostgreSQL database management.
* SQLAlchemy ORM.
* Alembic database migrations.
* Pydantic data validation.
* Separation of routes, services, models, and schemas.

> **Project status:** This README describes the current backend structure. Some features and API details may change as development continues.

## Features

* JWT-based authentication.
* Secure password hashing.
* User management.
* Blog post management.
* Categories and tags.
* Comments.
* PostgreSQL database integration.
* SQLAlchemy ORM.
* Alembic database migrations.
* Pydantic request and response validation.
* Interactive API documentation with Swagger UI and ReDoc.
* Environment-based configuration.

## Tech Stack

| Technology                                 | Purpose                           |
| ------------------------------------------ | --------------------------------- |
| [Python](https://www.python.org/)          | Programming language              |
| [FastAPI](https://fastapi.tiangolo.com/)   | API framework                     |
| [SQLAlchemy](https://www.sqlalchemy.org/)  | Database ORM                      |
| [PostgreSQL](https://www.postgresql.org/)  | Relational database               |
| [Alembic](https://alembic.sqlalchemy.org/) | Database migrations               |
| [Pydantic](https://docs.pydantic.dev/)     | Data validation and serialization |
| JWT                                        | Authentication                    |
| Git                                        | Version control                   |

## Project Structure

```text
dev-blog-app/
│
├── auth/
│   ├── auth_bearer.py
│   ├── auth_handler.py
│   └── __init__.py
│
├── core/
│   ├── config.py
│   ├── db_config.py
│   ├── dependency.py
│   └── __init__.py
│
├── models/
│   ├── categories.py
│   ├── comments.py
│   ├── join_tables.py
│   ├── posts.py
│   ├── tags.py
│   ├── token.py
│   ├── users.py
│   └── __init__.py
│
├── routes/
│   ├── auth_routes.py
│   ├── category_routes.py
│   ├── comment_routes.py
│   ├── post_routes.py
│   ├── tag_routes.py
│   ├── user_routes.py
│   └── __init__.py
│
├── schemas/
│   ├── category.py
│   ├── comment.py
│   ├── post.py
│   ├── tag.py
│   ├── token.py
│   ├── user.py
│   └── __init__.py
│
├── services/
│   ├── auth_services.py
│   ├── category_services.py
│   ├── comment_services.py
│   ├── post_services.py
│   ├── tag_services.py
│   ├── user_services.py
│   └── __init__.py
│
├── utils/
│   ├── enums.py
│   ├── helpers.py
│   └── __init__.py
│
├── .gitignore
├── main.py
├── README.md
├── Dockerfile
├── LICENSE
└── requirements.txt
```

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:

* Python 3.9 or higher.
* PostgreSQL.
* Git.
* A terminal or command-line interface.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dev_blog_app.git
cd dev_blog_app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows — PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows — Command Prompt**

```cmd
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
SECRET_KEY=your_secret_key
```

Replace the example values with your actual PostgreSQL credentials and application secret.

### 6. Run Database Migrations

If Alembic is configured in the project, apply the existing migrations:

```bash
alembic upgrade head
```

If you are setting up the database for the first time, make sure PostgreSQL is running and the database specified in `DATABASE_URL` exists.

### 7. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

| Documentation  | URL                                  |
| -------------- | ------------------------------------ |
| Swagger UI     | `http://127.0.0.1:8000/docs`         |
| ReDoc          | `http://127.0.0.1:8000/redoc`        |
| OpenAPI Schema | `http://127.0.0.1:8000/openapi.json` |

You can use Swagger UI to explore available endpoints, inspect request and response schemas, and test API requests.

## API Usage

### Example Request

The following example checks the application's root endpoint:

```bash
curl -X GET http://127.0.0.1:8000/
```

### Example Response

```json
{
  "message": "Welcome to Dev Blog App"
}
```

### Authentication

Protected endpoints require a valid JWT access token.

Include the token in the request header:

```http
Authorization: Bearer <your_access_token>
```

For the exact authentication endpoints and request formats, refer to the Swagger documentation.

## Database

Encore Hub uses PostgreSQL as its relational database and SQLAlchemy as its ORM.

The project includes models for:

* Users.
* Posts.
* Categories.
* Tags.
* Comments.
* Tokens.
* Many-to-many relationships through join tables.

Alembic is used to manage database schema changes.

### Common Migration Commands

Create a new migration:

```bash
alembic revision --autogenerate -m "Describe your changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Revert the latest migration:

```bash
alembic downgrade -1
```

> Run migration commands from the project directory containing your Alembic configuration.

## Security Considerations

Security is an important part of Encore Hub's backend design.

The project includes:

* **JWT authentication** for protected API endpoints.
* **Password hashing** instead of storing plain-text passwords.
* **Environment variables** for sensitive configuration.
* **Pydantic validation** for incoming request data.
* **Authentication and authorization** where required.
* **Response schemas** to control the data returned by the API.

### Security Best Practices

When deploying or extending the project:

* Never return password hashes in API responses.
* Never commit secrets to version control.
* Use a strong, randomly generated secret key.
* Use HTTPS in production.
* Keep dependencies updated.
* Validate and sanitize incoming data.
* Apply appropriate authorization checks.
* Avoid exposing sensitive information in error responses.
* Configure production database credentials securely.

## Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Clone your fork.
3. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

4. Make your changes.
5. Test your changes.
6. Commit your changes.

```bash
git add .
git commit -m "Add your feature"
```

7. Push your branch.

```bash
git push origin feature/your-feature
```

8. Open a pull request.

Please ensure your changes follow the existing project structure and coding conventions.

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more information.

## Author

**Tunmise Ola**

* GitHub: [@tunmi-stom](https://github.com/tunmi-stom)
* LinkedIn: [Tunmise Ola](https://www.linkedin.com/in/tunmi-stom/)
* Website: [tunmistom.name.ng](https://tunmistom.name.ng)

---

<p align="center">
  Built with Python, FastAPI, and PostgreSQL.
</p>
