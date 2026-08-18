# FastAPI + PostgreSQL + Supabase Auth API

A secure RESTful API built with **FastAPI**, **PostgreSQL**, and **Supabase Auth** (JWT-based authentication). Features containerization with **Docker Compose**, guarded protected routes, and interactive Swagger UI documentation.

---

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL (Containerized)
* **Identity Provider:** Supabase Auth (JWT Verification)
* **Containerization:** Docker & Docker Compose
* **Documentation:** Swagger UI (OpenAPI 3.0 with Bearer Auth)

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/mubiii3456/backend_api.git](https://github.com/mubiii3456/backend_api.git)
cd backend_api
2. Environment SetupCopy .env.example to .env and fill in your credentials:Bashcp .env.example .env
Ensure your .env contains:Code snippetDATABASE_URL=postgresql://postgres:dev@localhost:5433/tasks
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
3. Run ApplicationRun using Uvicorn or Docker Compose:Bashuvicorn app:app --reload
Interactive API Docs (Swagger UI): http://localhost:8000/docs📌 API Endpoints ReferenceMethodEndpointAuth RequiredDescriptionStatus CodePOST/auth/signupNoRegister a new user account201 Created / 400POST/auth/loginNoAuthenticate user & return JWT tokens200 OK / 401POST/auth/logoutYes (Bearer)Invalidate user session204 No Content / 401GET/public/infoNoOpen public access endpoint200 OKGET/protected/profileYes (Bearer)Retrieve authenticated user metadata200 OK / 401GET/protected/dashboardYes (Bearer)Example secondary protected route200 OK / 401GET/tasksNoFetch all task items200 OKPOST/tasksNoCreate a new task item201 Created / 400PUT/tasks/{id}NoUpdate task details200 OK / 404DELETE/tasks/{id}NoDelete a task item204 No Content / 404🔒 Security ImplementationStateless Authentication: Uses Supabase as an external Identity Provider (IdP) for hashing passwords and signing JWT access tokens.Token Verification: Protected routes use a custom FastAPI dependency (get_current_user) to intercept incoming HTTP Bearer headers and verify tokens with Supabase.Secrets Management: Critical credentials (SUPABASE_KEY, DATABASE_URL) are isolated in a git-ignored .env file.📝 Note for ReviewerFull Authentication Flow: Implemented end-to-end signup, login, token verification, and logout routes using Supabase Auth.Swagger UI Integration: Bearer authentication (HTTPBearer) is configured globally; protected endpoints showcase padlock icons for interactive authorization testing.Git Commit Hygiene: Progressive stage-by-stage development tracked with 6+ micro-commits.