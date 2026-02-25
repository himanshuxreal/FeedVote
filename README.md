# 📌 FeedVote

### DevOps-Based Feedback & Voting Web Application

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
User → Streamlit Frontend → FastAPI Backend → MySQL Database
                                    ↓
                                Dockerized
                                    ↓
                            GitHub Actions CI
```

---

# 🧰 4. Tech Stack

| Layer            | Technology     |
| ---------------- | -------------- |
| Frontend         | Streamlit      |
| Backend          | FastAPI        |
| Database         | MySQL          |
| SCM              | Git & GitHub   |
| CI/CD            | GitHub Actions |
| Containerization | Docker         |
| Testing          | Pytest         |

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

# 🗄 6. Database Structure (MySQL)

### 📌 Table: users

| Field      | Type                     | Description       |
| ---------- | ------------------------ | ----------------- |
| id         | INT (PK, AUTO_INCREMENT) | User ID           |
| username   | VARCHAR(100)             | Unique username   |
| email      | VARCHAR(100)             | User email        |
| created_at | TIMESTAMP                | Registration time |

---

### 📌 Table: feedback

| Field       | Type                     | Description |
| ----------- | ------------------------ | ----------- |
| id          | INT (PK, AUTO_INCREMENT) |             |
| title       | VARCHAR(255)             |             |
| description | TEXT                     |             |
| user_id     | INT (FK → users.id)      |             |
| created_at  | TIMESTAMP                |             |

---

### 📌 Table: votes

| Field       | Type                       | Description |
| ----------- | -------------------------- | ----------- |
| id          | INT (PK, AUTO_INCREMENT)   |             |
| feedback_id | INT (FK → feedback.id)     |             |
| user_id     | INT (FK → users.id)        |             |
| vote_type   | ENUM('upvote', 'downvote') |             |
| created_at  | TIMESTAMP                  |             |

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

* Base: python:3.10
* Install dependencies
* Run uvicorn

### Frontend Dockerfile

* Base: python:3.10
* Install streamlit
* Run streamlit app

---

# 🐳 docker-compose.yml

```yaml
version: "3.9"

services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: feedvote
    ports:
      - "3306:3306"

  backend:
    build: ./backend
    depends_on:
      - db
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    ports:
      - "8501:8501"
```

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

```bash
git clone https://github.com/yourusername/feedvote.git
cd feedvote
docker-compose up --build
```

Frontend:

```
http://localhost:8501
```

Backend:

```
http://localhost:8000/docs
```