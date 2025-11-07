# Project Overview

This is a full-stack web application powered by a Nuxt.js frontend and a FastAPI backend. The entire application is containerized using Docker and managed with Docker Compose.

## Architecture

The application is composed of three main services:

*   **`farout_frontend`**: A Nuxt.js application responsible for the user interface. It's a server-side rendered (SSR) application that communicates with the backend via HTTP requests.
*   **`farout_backend`**: A FastAPI application that serves as the API for the frontend. It handles business logic and interacts with the PostgreSQL database.
*   **`db`**: A PostgreSQL database that stores the application's data.

## Building and Running

The application is designed to be run with Docker Compose.

**To build and run the application:**

```bash
docker-compose up --build
```

This command will build the Docker images for the frontend and backend services and start all three services.

**To run the application in detached mode:**

```bash
docker-compose up -d
```

**To stop the application:**

```bash
docker-compose down
```

## Development Conventions

### Backend

*   The backend is a Python application built with the FastAPI framework.
*   Dependencies are managed with `pip` and are listed in `backend/requirements.txt`.
*   The backend uses SQLAlchemy for database interaction.

### Frontend

*   The frontend is a TypeScript application built with the Nuxt.js framework.
*   Dependencies are managed with `npm` and are listed in `frontend/package.json`.
*   The frontend uses SCSS for styling.

### TODO

*   Add instructions for running tests.
*   Add instructions for contributing to the project.
