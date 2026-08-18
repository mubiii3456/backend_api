# FastAPI + PostgreSQL Task API (Containerized)

A RESTful Task Management CRUD API built with **FastAPI** and **PostgreSQL**, fully containerized using **Docker** and **Docker Compose**.

---

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **Driver:** `psycopg` (v3)
* **Containerization:** Docker & Docker Compose

---

## 🚀 Quick Start

Follow these steps to run the complete stack on your local machine with a single command.

### 1. Clone the Repository
```bash
git clone <https://github.com/mubiii3456/backend_api>
cd backend_api
2. Configure Environment VariablesCopy the template .env.example file to create your .env file:Bashcp .env.example .env
3. Start the ApplicationRun the entire stack (FastAPI Backend + PostgreSQL Database) in detached mode:Bashdocker compose up -d
The API will be available at: http://localhost:8000Interactive API Documentation (Swagger UI): http://localhost:8000/docs📌 API EndpointsMethodEndpointDescriptionStatus CodeGET/Health check / Welcome message200 OKGET/tasksFetch all tasks200 OKGET/tasks/{id}Fetch a single task by ID200 OK / 404 Not FoundPOST/tasksCreate a new task201 Created / 400 Bad RequestPUT/tasks/{id}Update task title and status200 OK / 400 / 404DELETE/tasks/{id}Delete a task204 No Content / 404🧪 Sample Output (curl)Bashcurl -i http://localhost:8000/tasks
HTTPHTTP/1.1 200 OK
date: Tue, 18 Aug 2026 12:00:00 GMT
server: uvicorn
content-length: 198
content-type: application/json

[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": true
  },
  {
    "id": 2,
    "title": "Connect Postgres DB",
    "done": false
  },
  {
    "id": 3,
    "title": "Submit Week 3 Assignment",
    "done": false
  }
]
📸 Database Verification ScreenshotBelow is the screenshot confirming the database connection and the seeded tasks inside the Postgres Docker container: <img width="1164" height="182" alt="Screenshot 2026-08-18 115929" src="https://github.com/user-attachments/assets/e5f88311-bb40-4778-8e7d-6067c3443853" />
 
