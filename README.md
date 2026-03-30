# 📌 FeedVote

### DevOps-Based Feedback & Voting Web Application

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
name: FeedVote CI/CD Pipeline

# Trigger on push to main branch and pull requests
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  BACKEND_IMAGE: feedvote-backend
  FRONTEND_IMAGE: feedvote-frontend

jobs:
  # ====================
  # BACKEND BUILD & TEST
  # ====================
  backend-test:
    name: Backend Tests
    runs-on: ubuntu-latest
    
    # Set defaults for backend job
    defaults:
      run:
        working-directory: backend

    steps:
      # Clone repository
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for better diff detection

      # Setup Python environment
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      # Cache pip dependencies (speeds up CI)
      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-backend-${{ hashFiles('backend/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-backend-

      # Upgrade pip and install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Run tests with coverage
      - name: Run tests with pytest
        env:
          DATABASE_URL: "sqlite:///./test.db"
        run: |
          pytest tests/ -v \
            --tb=short \
            --cov=app \
            --cov-report=xml \
            --cov-report=html \
            --cov-report=term

      # Upload coverage reports
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend
          fail_ci_if_error: false

      # Code quality check with flake8 (strict)
      - name: Lint with flake8
        run: |
          # Install flake8
          pip install flake8
          
          # Stop the build if there are Python syntax errors or undefined names
          flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
          
          # Exit-zero treats all errors as warnings
          flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        continue-on-error: false

      # Static code analysis with pylint (optional)
      - name: Analyze with pylint
        run: |
          pip install pylint
          pylint app/ --exit-zero --max-line-length=127 || true
        continue-on-error: true

  # ====================
  # FRONTEND BUILD & TEST
  # ====================
  frontend-test:
    name: Frontend Tests
    runs-on: ubuntu-latest
    
    defaults:
      run:
        working-directory: frontend

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Cache pip dependencies (frontend)
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-frontend-${{ hashFiles('frontend/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-frontend-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Check if frontend runs without errors
      - name: Validate Streamlit app
        run: |
          streamlit config show
          python -c "import streamlit; print('✓ Streamlit import successful')"
        continue-on-error: false

  # ====================
  # SECURITY SCANNING
  # ====================
  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-security-${{ hashFiles('backend/requirements.txt', 'frontend/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-security-

      # Bandit: Security issue scanner for Python
      - name: Scan for security issues with Bandit
        run: |
          pip install bandit
          bandit -r backend/app/ frontend/ -f screen -ll || true
        continue-on-error: true

      # Safety: Check dependencies for known vulnerabilities
      - name: Check dependencies for vulnerabilities
        run: |
          pip install safety
          safety check --json || true
        continue-on-error: true

      # Check for hardcoded secrets
      - name: Detect secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --debug
        continue-on-error: true

  # ====================
  # DOCKER BUILD
  # ====================
  docker-build:
    name: Docker Build & Validation
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]  # Wait for tests to pass

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # Build backend Docker image
      - name: Build backend Docker image
        run: |
          echo "Building backend image..."
          docker build \
            --tag ${{ env.BACKEND_IMAGE }}:latest \
            --tag ${{ env.BACKEND_IMAGE }}:${{ github.sha }} \
            --file backend/Dockerfile \
            ./backend
          echo "✓ Backend image built successfully"

      # Build frontend Docker image
      - name: Build frontend Docker image
        run: |
          echo "Building frontend image..."
          docker build \
            --tag ${{ env.FRONTEND_IMAGE }}:latest \
            --tag ${{ env.FRONTEND_IMAGE }}:${{ github.sha }} \
            --file frontend/Dockerfile \
            ./frontend
          echo "✓ Frontend image built successfully"

      # Validate Docker Compose configuration
      - name: Validate docker-compose configuration
        run: |
          echo "Validating development configuration..."
          docker-compose config > /dev/null
          echo "✓ Development config validated"
          
          echo "Validating production configuration..."
          docker-compose -f docker-compose.prod.yml config > /dev/null
          echo "✓ Production config validated"

      # Check image sizes
      - name: Check Docker image sizes
        run: |
          echo "Backend image size:"
          docker images ${{ env.BACKEND_IMAGE }} --format "table {{.Repository}}\t{{.Size}}"
          echo ""
          echo "Frontend image size:"
          docker images ${{ env.FRONTEND_IMAGE }} --format "table {{.Repository}}\t{{.Size}}"

  # ====================
  # INTEGRATION TESTS
  # ====================
  integration-test:
    name: Integration Tests (Docker)
    runs-on: ubuntu-latest
    needs: docker-build

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # Build images for testing
      - name: Build Docker images
        run: |
          docker build -t feedvote-backend:test ./backend
          docker build -t feedvote-frontend:test ./frontend

      # Start services with Docker Compose
      - name: Start services with Docker Compose
        run: |
          docker-compose up -d
          echo "Waiting for services to be healthy..."
          sleep 10

      # Check backend health
      - name: Verify backend health
        run: |
          echo "Checking backend health..."
          for i in {1..30}; do
            if curl -f http://localhost:8000/health; then
              echo "✓ Backend is healthy"
              exit 0
            fi
            echo "Attempt $i: Waiting for backend..."
            sleep 2
          done
          echo "✗ Backend failed to start"
          docker-compose logs backend
          exit 1

      # Check API endpoints
      - name: Test API endpoints
        run: |
          echo "Testing API endpoints..."
          
          # Root endpoint
          curl -f http://localhost:8000/ || exit 1
          echo "✓ Root endpoint working"
          
          # Health endpoint
          curl -f http://localhost:8000/health || exit 1
          echo "✓ Health endpoint working"
          
          # API documentation
          curl -f http://localhost:8000/docs || exit 1
          echo "✓ API docs endpoint working"

      # Cleanup
      - name: Stop Docker services
        if: always()
        run: |
          echo "Stopping services..."
          docker-compose down -v
          echo "✓ Services stopped and volumes removed"

      # Save logs
      - name: Save service logs
        if: always()
        run: |
          docker-compose logs > service-logs.txt || true

      # Upload logs as artifact
      - name: Upload service logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: service-logs
          path: service-logs.txt

  # ====================
  # FINAL STATUS
  # ====================
  status:
    name: Build Status
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test, security-scan, docker-build, integration-test]
    if: always()

    steps:
      - name: Check job status
        run: |
          if [ "${{ needs.backend-test.result }}" != "success" ]; then
            echo "❌ Backend tests failed"
            exit 1
          fi
          if [ "${{ needs.frontend-test.result }}" != "success" ]; then
            echo "❌ Frontend validation failed"
            exit 1
          fi
          if [ "${{ needs.docker-build.result }}" != "success" ]; then
            echo "❌ Docker build failed"
            exit 1
          fi
          if [ "${{ needs.integration-test.result }}" != "success" ]; then
            echo "❌ Integration tests failed"
            exit 1
          fi
          echo "✓ All checks passed!"

      - name: Notify success
        if: success()
        run: |
          echo "✅ Pipeline completed successfully"
          echo "Commit: ${{ github.sha }}"
          echo "Branch: ${{ github.ref }}"
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