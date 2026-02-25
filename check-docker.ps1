# Docker Installation Check Script for Windows PowerShell
# Usage: .\check-docker.ps1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Docker Installation Check" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[+] Docker is installed" -ForegroundColor Green
        Write-Host "    $dockerVersion" -ForegroundColor Green
    } else {
        throw "Docker not found"
    }
} catch {
    Write-Host "[!] Docker is NOT installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Docker Desktop on Windows:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Download Docker Desktop from:" -ForegroundColor Yellow
    Write-Host "   https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Run the installer and follow the setup wizard" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Enable WSL 2 during installation" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "4. Restart your computer" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "5. Verify installation by running:" -ForegroundColor Yellow
    Write-Host "   docker --version" -ForegroundColor Cyan
    Write-Host "   docker-compose --version" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host ""

# Check if Docker Compose is installed
try {
    $composeVersion = docker-compose --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[+] Docker Compose is installed" -ForegroundColor Green
        Write-Host "    $composeVersion" -ForegroundColor Green
    } else {
        throw "Docker Compose not found"
    }
} catch {
    Write-Host "[!] Docker Compose is NOT installed" -ForegroundColor Red
    Write-Host "    (Note: Docker Desktop includes Docker Compose)" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if Docker daemon is running
try {
    docker ps >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[+] Docker daemon is running" -ForegroundColor Green
    } else {
        throw "Docker daemon not responding"
    }
} catch {
    Write-Host "[!] Docker daemon is NOT running" -ForegroundColor Red
    Write-Host "    Please start Docker Desktop application" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "All checks passed!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use Docker to run FeedVote:" -ForegroundColor Green
Write-Host ""
Write-Host "  Navigate to the FeedVote directory:" -ForegroundColor Yellow
Write-Host "  cd c:\Users\srbro\Dropbox\PC\Desktop\FeedVote" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Build the Docker images:" -ForegroundColor Yellow
Write-Host "  docker-compose build" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Start the application:" -ForegroundColor Yellow
Write-Host "  docker-compose up -d" -ForegroundColor Cyan
Write-Host ""
Write-Host "  View logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Access the application:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
