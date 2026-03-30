# 📌 FeedVote (Feedback and Voting)

### DevOps-Based Feedback & Voting Web Application (Module) 

---

## ✅ **CURRENT STATUS** (March 30, 2026)

- ✅ **Backend (FastAPI):** Running on `http://localhost:8000`
- ✅ **Frontend (Streamlit):** Running on `http://localhost:8501`
- ✅ **Database (SQLite):** Fully functional with 3 tables and persistent data
- ✅ **API Documentation:** Available at `http://localhost:8000/docs`
- ✅ **All core features:** Working and tested
- ✅ **Docker:** Configured and ready (requires Docker Desktop running)

**Latest Verification:** Database verified with proper relationships ✓ | All API endpoints functional ✓ | Data persistence confirmed ✓

---

# 📖 1. Project Overview

**FeedVote** is a lightweight web application that allows users to:

* Submit feedback
* Post ideas
* Vote on ideas
* View most popular suggestions

The primary objective of this project is **not application complexity**, but to demonstrate a complete DevOps lifecycle implementation, including:

* Source Code Management (SCM)
* Continuous Integration (CI)
* Containerization
* Automated Build Pipeline
* Deployment-ready architecture

---

# 🎯 2. Project Goals

This project demonstrates:

* Proper Git workflow
* CI pipeline using GitHub Actions
* Docker-based containerization
* Backend–Frontend separation
* SQLite database integration
* Clean DevOps pipeline structure

---

# 🏗 3. System Architecture

```
User Browser
    ↓
Streamlit Frontend (Port 8501)
    ↓
FastAPI Backend (Port 8000)
    ↓
SQLite Database (feedvote.db - File-based, No server required)
    ↓
[Optional] Docker Containers (For deployment)
```

---

# 🧰 4. Tech Stack

| Layer            | Technology          |
| ---------------- | ------------------- |
| Frontend         | Streamlit 1.28.1    |
| Backend          | FastAPI 0.104.1     |
| Backend Server   | Uvicorn 0.24.0      |
| Database         | SQLite 3 (File-based) |
| ORM              | SQLAlchemy 2.0.23   |
| Validation       | Pydantic 2.5.0      |
| HTTP Client      | Requests 2.31.0     |
| SCM              | Git & GitHub        |
| CI/CD            | GitHub Actions      |
| Containerization | Docker & Docker Compose |
| Testing          | Pytest 7.4.3        |

---

# 📂 5. Project Folder Structure

```
FeedVote/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── crud.py
│   │   └── routes/
│   │       ├── users.py
│   │       ├── feedback.py
│   │       └── vote.py
│   │
│   ├── tests/
│   │   ├── test_feedback.py
│   │   └── test_vote.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── LICENSE
```

---

# 🗄 6. Database Structure (SQLite)

### 📍 Database File
- **Location:** `backend/feedvote.db`
- **Type:** SQLite 3 (File-based, no server required)
- **Persistence:** Data persists across application restarts
- **Auto-initialization:** Database and tables created automatically on backend startup

### 📌 Table: users

| Field      | Type                | Description       |
| ---------- | ------------------- | ----------------- |
| id         | INTEGER PRIMARY KEY | User ID (auto)    |
| username   | VARCHAR(100)        | Unique username   |
| email      | VARCHAR(100)        | Unique user email |
| created_at | DATETIME            | Registration time |

**Indexes:** ix_users_id, ix_users_username (unique), ix_users_email (unique)

---

### 📌 Table: feedback

| Field       | Type                | Description          |
| ----------- | ------------------- | -------------------- |
| id          | INTEGER PRIMARY KEY | Feedback ID (auto)   |
| title       | VARCHAR(255)        | Feedback title       |
| description | TEXT                | Detailed description |
| user_id     | INTEGER (FK)        | Reference to users   |
| created_at  | DATETIME            | Creation timestamp   |

**Indexes:** ix_feedback_id, ix_feedback_title, ix_feedback_created_at, ix_feedback_user_id

**Foreign Key:** user_id → users.id

---

### 📌 Table: votes

| Field       | Type                | Description              |
| ----------- | ------------------- | ------------------------ |
| id          | INTEGER PRIMARY KEY | Vote ID (auto)           |
| feedback_id | INTEGER (FK)        | Reference to feedback    |
| user_id     | INTEGER (FK)        | Reference to user        |
| vote_type   | VARCHAR(8)          | 'upvote' or 'downvote'   |
| created_at  | DATETIME            | Vote timestamp           |

**Indexes:** ix_votes_id, ix_votes_feedback_id, ix_votes_user_id, ix_votes_created_at

**Foreign Keys:** feedback_id → feedback.id, user_id → users.id

**Additional Logic:** 
- Users cannot vote on their own feedback
- Duplicate votes update the existing vote rather than create a new one

---

# 🎨 7. Frontend Design (Streamlit)

### 🖥 Application Pages

The Streamlit frontend provides a user-friendly interface with the following pages:

#### 🔹 Authentication (Sidebar)
- **Login:** Users can log in with their username
- **Register:** New users can create an account with username and email
- **Logout:** Authenticated users can log out at any time
- **User Display:** Shows currently logged-in username

#### 🔹 Home Page
- Welcome message and application overview
- Instructions on how to use the platform
- Prompts users to login/register to get started

#### 🔹 Submit Feedback Page
- **Access:** Login required
- **Form elements:**
  - Title input (max 255 characters)
  - Description text area
  - Submit button
- **Functionality:** Submit new ideas/feedback to the platform

#### 🔹 View Ideas Page
- **Access:** Available to all users (login not required for viewing)
- **Features:**
  - Display all feedback ideas in a list format
  - Each feedback card shows:
    - Title
    - Description
    - Author information and timestamp
    - Upvote/Downvote buttons (if logged in)
  - Empty state message if no ideas exist

#### 🔹 Top Voted Ideas Page (Leaderboard)
- **Features:**
  - Displays top 20 most voted ideas sorted by vote count
  - Medal rankings (🥇, 🥈, 🥉) for top 3
  - Score display showing net votes with upvote/downvote breakdown
  - Author information and creation timestamp
  - Vote buttons for logged-in users
  - Empty state message if no votes exist

# 🔌 8. API Endpoints (FastAPI)

### 📍 Base URL
- Local: `http://localhost:8000`
- Documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative Docs (ReDoc): `http://localhost:8000/redoc`

### 🔹 Health & Info Endpoints

| Method | Endpoint   | Description         | Status Code |
| ------ | ---------- | ------------------- | ----------- |
| GET    | /          | Root endpoint       | 200         |
| GET    | /health    | Health check        | 200         |

### 🔹 User Endpoints

| Method | Endpoint              | Description           | Status Code |
| ------ | --------------------- | --------------------- | ----------- |
| POST   | /users/               | Create new user       | 201         |
| GET    | /users/{username}     | Get user by username  | 200         |
| GET    | /users/id/{user_id}   | Get user by ID        | 200         |

**Request body (POST /users/):**
```json
{
  "username": "string (3-100 chars, unique)",
  "email": "string (valid email, unique)"
}
```

### 🔹 Feedback Endpoints

| Method | Endpoint        | Description                | Status Code |
| ------ | --------------- | -------------------------- | ----------- |
| POST   | /feedback/      | Create new feedback        | 201         |
| GET    | /feedback/      | Get all feedback (paginated) | 200        |
| GET    | /feedback/{id}  | Get specific feedback by ID | 200         |

**Request body (POST /feedback/?user_id={user_id}):**
```json
{
  "title": "string (1-255 chars)",
  "description": "string (minimum 1 char)"
}
```

**Query parameters (GET /feedback/):**
- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 100, max: 100)

### 🔹 Vote Endpoints

| Method | Endpoint      | Description           | Status Code |
| ------ | ------------- | --------------------- | ----------- |
| POST   | /vote/        | Submit upvote/downvote | 201        |
| GET    | /vote/top/    | Get top voted ideas   | 200         |

**Request body (POST /vote/):**
```json
{
  "feedback_id": "integer (>0)",
  "user_id": "integer (>0)",
  "vote_type": "string (upvote or downvote)"
}
```

**Query parameters (GET /vote/top/):**
- `limit`: Number of top ideas to return (default: 10, max: 100)

---

# 🧪 9. Test Cases (Pytest)

### 📌 test_feedback.py

* Test feedback creation
* Test feedback retrieval
* Test invalid input

Example:

```python
def test_create_feedback(client):
    response = client.post("/feedback/", json={
        "title": "Improve UI",
        "description": "Add dark mode"
    })
    assert response.status_code == 201
```

---

### 📌 test_vote.py

* Test upvote
* Test duplicate vote prevention
* Test vote count increment

---

# 🐳 10. Docker Setup

### Backend Dockerfile
- **Base Image:** python:3.10
- **Features:**
  - Install dependencies from requirements.txt
  - Run FastAPI with uvicorn on port 8000
  - Auto-create SQLite database on startup
  - Database tables initialized automatically via SQLAlchemy ORM

### Frontend Dockerfile
- **Base Image:** python:3.10
- **Features:**
  - Install Streamlit 1.28.1
  - Configure Streamlit for remote access (required for Docker)
  - Auto-connect to backend service via network
  - Exposes port 8501 for web interface

---

# 🐳 Docker Compose Configuration

```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    container_name: feedvote-backend
    environment:
      DATABASE_URL: "sqlite:///./feedvote.db"
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    networks:
      - feedvote-network
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: feedvote-frontend
    depends_on:
      - backend
    environment:
      BACKEND_URL: "http://backend:8000"
    ports:
      - "8501:8501"
    volumes:
      - ./frontend:/app
    networks:
      - feedvote-network
    restart: unless-stopped

networks:
  feedvote-network:
    driver: bridge
```

**Key Points:**
- SQLite database file persists in container volumes
- Services communicate via custom network
- Port mapping: Backend 8000, Frontend 8501

---

# 🔄 11. DevOps Workflow

### Step 1 — Developer Pushes Code

* Git tracks changes
* Version control maintained

### Step 2 — GitHub Actions CI Triggered

* Install dependencies
* Run tests
* Build Docker image
* Fail if tests fail

---

# ⚙️ 12. GitHub Actions CI Pipeline (.github/workflows/ci.yml)

```yaml
name: FeedVote CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install backend dependencies
        run: |
          cd backend
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run backend tests (Pytest)
        run: |
          cd backend
          pytest

      - name: Build backend Docker image
        run: docker build -t feedvote-backend ./backend

      - name: Build frontend Docker image
        run: docker build -t feedvote-frontend ./frontend
```

### Pipeline Details:
- **Triggers:** On push to main branch and pull requests
- **Runner:** Ubuntu latest
- **Python Version:** 3.10
- **Steps:**
  1. Checkout code
  2. Set up Python environment
  3. Install dependencies from requirements.txt
  4. Run Pytest tests
  5. Build Docker images for both backend and frontend
- **Database:** Uses SQLite (file-based, no external service needed)

---

# 🔐 13. Security Considerations

* **Vote Integrity:** Users cannot vote on their own feedback (enforced at API level)
* **Duplicate Votes:** Same user voting on same feedback multiple times updates the existing vote rather than creating duplicates
* **Input Validation:** All requests validated using Pydantic schemas with field constraints
  - Username: 3-100 characters
  - Email: Valid email format (EmailStr)
  - Feedback title: 1-255 characters
  - Vote type: Only 'upvote' or 'downvote' allowed
* **CORS Configuration:** Cross-Origin Resource Sharing enabled for all origins (suitable for development; restrict in production)
* **Database:** SQLite file-based (secure location recommended in production)
* **Unique Constraints:** Usernames and emails are unique at database level

---

# 📜 14. License

This project is licensed under the MIT License.

---

# 🚀 15. How to Run Locally

## Quick Start (No Docker Required)

### Prerequisites
- Python 3.10 or 3.11
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/feedvote.git
cd feedvote
```

### Step 2: Setup Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1          # On Windows
# source venv/bin/activate           # On Linux/Mac
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Run Backend (Keep running)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will:**
- Create SQLite database automatically at `backend/feedvote.db`
- Initialize all tables (users, feedback, votes)
- Start API server: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Step 4: Setup Frontend (in New Terminal)
```powershell
cd frontend
python -m venv venv
.\venv\Scripts\Activate.ps1          # On Windows
# source venv/bin/activate           # On Linux/Mac
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Run Frontend
```powershell
cd frontend
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

**Frontend will:**
- Start on: `http://localhost:8501`
- Connect to backend automatically
- Open in browser automatically

---

## Docker Setup

### Prerequisites
- Docker Desktop installed and running
- Docker Compose

### Step 1: Build Images
```bash
cd feedvote
docker-compose build
```

### Step 2: Start Containers
```bash
docker-compose up -d
```

### Step 3: Check Status
```bash
docker-compose ps
```

### Step 4: View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Access Application
- **Frontend:** `http://localhost:8501`
- **Backend API:** `http://localhost:8000`
- **API Docs:** `http://localhost:8000/docs`

### Stop Containers
```bash
docker-compose down
```

---

## Accessing the Application

### Frontend UI
- **URL:** `http://localhost:8501`
- **Features:**
  - User registration and login
  - Submit feedback
  - View all feedback
  - Vote on feedback (upvote/downvote)
  - View top-voted ideas

### Backend API Documentation
- **URL:** `http://localhost:8000/docs` (Swagger UI)
- **Alternative:** `http://localhost:8000/redoc` (ReDoc)
- **Features:**
  - Interactive API explorer
  - Try out endpoints
  - See request/response examples

### Database
- **File:** `backend/feedvote.db`
- **Type:** SQLite 3
- **Persistence:** Automatic
- **Verification:** Run `backend/check_db.py` to verify database status

---

## Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Specific Test
```bash
cd backend
pytest tests/test_feedback.py -v
```

---

## Troubleshooting

### Backend won't start
- Ensure port 8000 is not in use: `netstat -ano | findstr :8000`
- Kill process: `taskkill /PID <PID> /F`

### Frontend can't connect to backend
- Verify backend is running first
- Check BACKEND_URL in `frontend/app.py` (default: `http://localhost:8000`)

### Database issues
- Delete `backend/feedvote.db` to reset
- Database will be recreated on next backend start

### Docker issues
- Ensure Docker Desktop is running
- Rebuild images: `docker-compose build --no-cache`