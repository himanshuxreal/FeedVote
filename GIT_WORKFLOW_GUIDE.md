# Git Workflow - Complete Instructions for Finishing the Fix

## Current Status
✅ All files have been modified locally  
✅ Database file removed from tracking  
✅ CI workflow fixed and re-encoded to UTF-8  
✅ Ready for commit and PR

---

## Step-by-Step Git Workflow

### **Step 1: Verify Current State**

```bash
cd c:\FeedVote
git branch -v
# Should show: * fix/ci-database-and-config
```

### **Step 2: Check Status of Changes**

```bash
git status

# Expected output:
# On branch fix/ci-database-and-config
# Changes not staged for commit:
#   deleted:    backend/feedvote.db
#   modified:   .gitignore
#   modified:   .env.example
#   modified:   .github/workflows/ci.yml
```

### **Step 3: Stage All Changes**

```bash
# Stage deleted file (database)
git add -A .
# OR explicitly:
git add backend/feedvote.db .gitignore .env.example .github/workflows/ci.yml
```

### **Step 4: Commit Changes**

```bash
git commit -m "fix(ci): fix encoding issues and database tracking

BREAKING CHANGE: Database files are no longer tracked in git

Changes:
- Fix GitHub Actions workflow UTF-8 encoding issue
  * Regenerated .github/workflows/ci.yml with proper UTF-8 encoding
  * Resolves GitHub Actions parser failures
  
- Remove database file from git tracking
  * Executed: git rm --cached backend/feedvote.db
  * Database files should never be in version control
  
- Update .gitignore with explicit database patterns
  * Added: *.db, *.sqlite, *.sqlite3, feedvote.db, test.db, *.db-journal
  * Ensures database files remain ignored
  
- Update .env.example with clarified documentation
  * Added comprehensive comments explaining dev vs production paths
  * Clarified MySQL environment variable usage

Database Isolation (Verified):
- Development: sqlite:///./feedvote.db (file not committed)
- Testing: sqlite:///./test.db (conftest.py - dynamic)
- Docker: /tmp/feedvote.db (isolated volume)
- Production: MySQL via environment variables

Fixes GitHub Actions Workflow:
- Encoding: cp1252 -> UTF-8 (required by GitHub)
- Syntax: Verified with Python YAML parser
- Actions: checkout@v4, setup-python@v4, cache@v4, upload-artifact@v4"