@echo off
REM Docker Installation Helper for Windows
REM This script checks for Docker and provides installation instructions

echo.
echo ==========================================
echo Docker Installation Check
echo ==========================================
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Docker is NOT installed or not in PATH
    echo.
    echo To install Docker Desktop on Windows:
    echo.
    echo 1. Download Docker Desktop from:
    echo    https://www.docker.com/products/docker-desktop
    echo.
    echo 2. Run the installer and follow the setup wizard
    echo.
    echo 3. Enable WSL 2 (Windows Subsystem for Linux 2^):
    echo    - In installer, check "Use WSL 2 instead of Hyper-V"
    echo    - Or manually enable in Windows Features
    echo.
    echo 4. Restart your computer
    echo.
    echo 5. Open PowerShell and verify installation:
    echo    docker --version
    echo    docker-compose --version
    echo.
    echo 6. Then run from the FeedVote directory:
    echo    docker-compose build
    echo    docker-compose up -d
    echo.
    exit /b 1
) else (
    echo [+] Docker is installed
    for /f "tokens=*" %%i in ('docker --version') do echo %%i
    echo.
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Docker Compose is NOT installed
    echo Note: Docker Desktop includes Docker Compose
    echo Ensure Docker Desktop is properly installed and in PATH
    echo.
    exit /b 1
) else (
    echo [+] Docker Compose is installed
    for /f "tokens=*" %%i in ('docker-compose --version') do echo %%i
    echo.
)

REM Check if Docker daemon is running
docker ps >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Docker daemon is NOT running
    echo Please start Docker Desktop application
    exit /b 1
) else (
    echo [+] Docker daemon is running
    echo.
)

echo ==========================================
echo All checks passed! You can now use Docker
echo ==========================================
echo.
echo Ready to build and run FeedVote:
echo   docker-compose build
echo   docker-compose up -d
