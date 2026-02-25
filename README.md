# 📌 FeedVote

### DevOps-Based Feedback & Voting Web Application

---

## ✅ **CURRENT STATUS** (February 25, 2026)

- ✅ **Backend (FastAPI):** Running on `http://localhost:8000`
- ✅ **Frontend (Streamlit):** Running on `http://localhost:8501`
- ✅ **Database (SQLite):** Fully functional with 3 tables and persistent data
- ✅ **API Documentation:** Available at `http://localhost:8000/docs`
- ✅ **All core features:** Working and tested
- ✅ **Docker:** Configured and ready (requires Docker Desktop running)

**Latest Verification:** Database tested with user creation ✓ | API endpoints tested ✓ | Data persistence confirmed ✓

---

# 📖 1. Project Overview

**FeedVote** is a lightweight web application that allows users to:

* Submit feedback
* Post ideas
* Vote on ideas
* View most popular suggestions

The primary objective of this project is **not application complexity**, but to demonstrate a complete DevOps lifecycle implementation**, including:

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
* MySQL database integration
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
| Database         | SQLite 3            |
| Server           | Uvicorn 0.24.0      |
| ORM              | SQLAlchemy 2.0.23   |
| Validation       | Pydantic 2.5.0      |
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
- **Size:** ~61 KB
- **Type:** SQLite 3 (File-based, no server required)
- **Persistence:** Data persists across application restarts

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
| vote_type   | VARCHAR(8)          | 'UPVOTE' or 'DOWNVOTE'   |
| created_at  | DATETIME            | Vote timestamp           |

**Indexes:** ix_votes_id, ix_votes_feedback_id, ix_votes_user_id, ix_votes_created_at

**Foreign Keys:** feedback_id → feedback.id, user_id → users.id

---

# 🎨 7. Frontend Design (Streamlit)

### 🖥 Layout Plan

### 🔹 Sidebar

* Login / Register
* Navigation:

  * Submit Feedback
  * View Ideas
  * Top Voted

---

### 🔹 Main Page Sections

#### 1️⃣ Submit Feedback Page

* Title Input
* Description Text Area
* Submit Button

---

#### 2️⃣ View Ideas Page

* List of ideas (cards)
* Each card contains:

  * Title
  * Description
  * Vote Count
  * Upvote Button
  * Downvote Button

---

#### 3️⃣ Top Ideas Page

* Sorted by highest vote count
* Display leaderboard style

---

# 🔌 8. API Endpoints (FastAPI)

| Method | Endpoint       | Description         |
| ------ | -------------- | ------------------- |
| POST   | /feedback/     | Create new feedback |
| GET    | /feedback/     | Get all feedback    |
| GET    | /feedback/{id} | Get single feedback |
| POST   | /vote/         | Submit vote         |
| GET    | /top/          | Get top voted ideas |

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
  - Run FastAPI with uvicorn
  - Auto-create SQLite database
  - Health checks enabled

### Frontend Dockerfile
- **Base Image:** python:3.10
- **Features:**
  - Install Streamlit 1.28.1
  - Configure for remote access
  - Auto-connect to backend

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

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run Tests
        run: |
          cd backend
          pytest

      - name: Build Docker
        run: docker build -t feedvote-backend ./backend
```

---

# 🔐 13. Security Considerations

* Prevent duplicate votes
* Use environment variables for DB credentials
* Input validation using Pydantic
* Docker secrets in production

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