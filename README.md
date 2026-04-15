# 🗳️ FeedVote

## 🎯 Problem Statement

FeedVote is a lightweight feedback and voting application for small teams and classroom projects. It simplifies idea submission, voting, and prioritization while demonstrating a complete DevOps workflow with containerization and automated CI/CD.

## 🏗️ System Architecture

The application uses a Streamlit frontend to collect and display feedback. The frontend sends requests to a FastAPI backend, which stores data in a SQLite database. Docker is used for containerization, GitHub Actions manages CI/CD, and Docker Hub is used for deployment.

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

## 🚀 CI/CD Pipeline Explanation

### ✅ Backend & Frontend Tests

The pipeline runs backend and frontend tests to validate API endpoints, database operations, and user interaction flows.

### 🔒 Security Scanning

Security scanning checks code and dependencies for vulnerabilities and exposed secrets using tools such as Bandit, Safety, and Trufflehog.

### 🐳 Docker Build & Validation

Docker build validates the backend and frontend container images and ensures the application can start successfully in the container environment.

### 🔗 Integration Testing

Integration testing uses Docker Compose to run backend, frontend, and database services together, verifying the full workflow end to end.

### 📦 Deployment

The final stage pushes the validated Docker image to Docker Hub so the application is available for deployment.

## 🌿 Git Workflow Used

The project follows a feature branch workflow. Developers create a feature branch, push changes, and open a pull request. The pull request triggers automated testing. Once tests pass, the branch is merged into main and deployment proceeds.

## 🛠️ Tools Used

| Tool | Purpose |
| --- | --- |
| ⚡ FastAPI | Backend API framework |
| 🎨 Streamlit | Frontend user interface |
| 🐳 Docker | Containerization runtime |
| 🎼 Docker Compose | Local service orchestration |
| 🤖 GitHub Actions | CI/CD automation |
| 📦 Docker Hub | Container image registry |
| 💾 SQLite | Lightweight relational database |

## 📸 Screenshots

### 🔹 Pipeline Success
![Pipeline Success](images/pipeline_success.png)

### 🔹 Deployment Output
![Deployment Output](images/deployment.png)

### 🔹 Application Running
![App Screenshot](images/frontend_running.png)

### 🔹 Deploy to Docker hub Job Success
![CI/CD Screenshot](images/deploy_job_success.png)

## ⚠️ Challenges Faced

* Docker image build and service startup issues
* CI/CD pipeline configuration and test failures
* Debugging application behavior across frontend, backend, and database
* Understanding localhost versus 0.0.0.0 for container access
* Docker Hub authentication and token management
