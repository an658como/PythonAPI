
# 🚀 Python API using FastAPI

## 🌟 Introduction
This project aims to develop the necessary REST API endpoints for a simple social media platform using **FastAPI**.

## ⚙️ Setup for Development Environment and Running the Server Locally

### 🐍 Virtual Environment
Create a virtual environment with your preferred name `<venv>`:

```bash
python3 -m venv <venv>
```

### 💻 Activate Virtual Environment (Linux)

```bash
<venv>/bin/activate
```

### 📦 Install Dependencies
To install all required dependencies:

```bash
pip install -r requirements.txt
```

### 🐘 Install PostgreSQL
You have two options to set up PostgreSQL:
1. **Install a local instance** of PostgreSQL and create an empty database named `fastapi`.
2. **Use Docker**: From the project root directory, run the following command to spin up PostgreSQL using Docker:

```bash
docker compose up -d
```

### 🛠️ Build the Database Tables
We use **Alembic** for database migrations. Run the following command to create the required tables in the database:

```bash
alembic upgrade head
```

## 🚀 Running the Server
To run the server locally:

```bash
uvicorn app.main:app --reload
```

## 📖 API Documentation
Once the server is running, the API documentation is automatically generated. You can access it by visiting:

```bash
http://127.0.0.1:8000/docs
```

Now you're all set to experiment with the available API endpoints! 🎉

Alternatively, you could play with the API on AWS without building the app locally:
[https://www.alinaseri.xyz/docs](https://www.alinaseri.xyz/docs)



---
🛠️ **Tech Stack**: Python, FastAPI, PostgreSQL, Alembic, Docker
