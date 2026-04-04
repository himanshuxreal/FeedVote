@echo off
REM FeedVote System Verification Script (Windows)
REM Run after `docker-compose up -d` to verify all services are healthy

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo FeedVote System Verification
echo ==========================================
echo.

set PASSED=0
set FAILED=0

REM Helper function to print pass
call :pass "Docker and Docker Compose ready"

echo.
echo 1. Checking Docker and Docker Compose...
echo.

REM Check Docker
docker --version > nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('docker --version') do (
        echo [PASS] Docker installed: %%i
        set /a PASSED+=1
    )
) else (
    echo [FAIL] Docker not installed
    set /a FAILED+=1
    exit /b 1
)

REM Check Docker Compose
docker-compose --version > nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('docker-compose --version') do (
        echo [PASS] Docker Compose installed: %%i
        set /a PASSED+=1
    )
) else (
    echo [FAIL] Docker Compose not installed
    set /a FAILED+=1
    exit /b 1
)

echo.
echo 2. Checking Docker Compose Configuration...
echo.

REM Validate compose file
docker-compose config > nul 2>&1
if !errorlevel! equ 0 (
    echo [PASS] docker-compose.yml is valid
    set /a PASSED+=1
) else (
    echo [FAIL] docker-compose.yml validation failed
    set /a FAILED+=1
    exit /b 1
)

echo.
echo 3. Checking Container Status...
echo.

REM Check if containers are running
docker ps --filter "name=feedvote-backend" --format "{{.Names}}" 2>nul | findstr /r "." > nul
if !errorlevel! equ 0 (
    echo [PASS] Backend container is running
    set /a PASSED+=1
) else (
    echo [FAIL] Backend container is not running
    set /a FAILED+=1
)

docker ps --filter "name=feedvote-frontend" --format "{{.Names}}" 2>nul | findstr /r "." > nul
if !errorlevel! equ 0 (
    echo [PASS] Frontend container is running
    set /a PASSED+=1
) else (
    echo [FAIL] Frontend container is not running
    set /a FAILED+=1
)

echo.
echo 4. Checking Container Health...
echo.

REM Check backend health state
for /f "tokens=*" %%i in ('docker inspect feedvote-backend 2^>nul ^| findstr /c:"Status" ^| findstr /c:"healthy"') do (
    set "BACKEND_HEALTH=healthy"
)

if "!BACKEND_HEALTH!"=="healthy" (
    echo [PASS] Backend container is healthy
    set /a PASSED+=1
) else (
    echo [FAIL] Backend container health check failed or still starting
    set /a FAILED+=1
)

REM Check frontend health state
for /f "tokens=*" %%i in ('docker inspect feedvote-frontend 2^>nul ^| findstr /c:"Status" ^| findstr /c:"healthy"') do (
    set "FRONTEND_HEALTH=healthy"
)

if "!FRONTEND_HEALTH!"=="healthy" (
    echo [PASS] Frontend container is healthy
    set /a PASSED+=1
) else (
    echo [FAIL] Frontend container health check failed or still starting
    set /a FAILED+=1
)

echo.
echo 5. Checking Network Connectivity...
echo.

REM Check backend health endpoint
powershell -Command "try { $response = curl.exe -sf http://localhost:8000/health; if ($?) { exit 0 } else { exit 1 } } catch { exit 1 }" 2>nul
if !errorlevel! equ 0 (
    echo [PASS] Backend health endpoint responding
    set /a PASSED+=1
) else (
    echo [FAIL] Backend health endpoint not responding
    set /a FAILED+=1
)

REM Check frontend
powershell -Command "try { $response = curl.exe -sf http://localhost:8501; if ($?) { exit 0 } else { exit 1 } } catch { exit 1 }" 2>nul
if !errorlevel! equ 0 (
    echo [PASS] Frontend is responding
    set /a PASSED+=1
) else (
    echo [FAIL] Frontend not responding
    set /a FAILED+=1
)

echo.
echo 6. Checking Readiness Markers...
echo.

REM Check backend readiness marker
docker exec feedvote-backend test -f /tmp/backend-ready > nul 2>&1
if !errorlevel! equ 0 (
    echo [PASS] Backend readiness marker exists
    set /a PASSED+=1
) else (
    echo [FAIL] Backend readiness marker missing
    set /a FAILED+=1
)

REM Check frontend readiness marker
docker exec feedvote-frontend test -f /tmp/frontend-ready > nul 2>&1
if !errorlevel! equ 0 (
    echo [PASS] Frontend readiness marker exists
    set /a PASSED+=1
) else (
    echo [FAIL] Frontend readiness marker missing
    set /a FAILED+=1
)

echo.
echo 7. Checking API Endpoints...
echo.

REM Root endpoint
powershell -Command "try { $response = curl.exe -sf http://localhost:8000/; if ($?) { exit 0 } else { exit 1 } } catch { exit 1 }" 2>nul
if !errorlevel! equ 0 (
    echo [PASS] Backend root endpoint ^(^/^) working
    set /a PASSED+=1
) else (
    echo [FAIL] Backend root endpoint ^(^/^) not working
    set /a FAILED+=1
)

REM API docs
powershell -Command "try { $response = curl.exe -sf http://localhost:8000/docs; if ($?) { exit 0 } else { exit 1 } } catch { exit 1 }" 2>nul
if !errorlevel! equ 0 (
    echo [PASS] Backend API documentation ^(/docs^) working
    set /a PASSED+=1
) else (
    echo [FAIL] Backend API documentation ^(/docs^) not working
    set /a FAILED+=1
)

echo.
echo ==========================================
echo Verification Summary
echo ==========================================
echo Tests Passed: %PASSED%
echo Tests Failed: %FAILED%
echo.

if %FAILED% equ 0 (
    echo [SUCCESS] All checks passed! System is healthy.
    echo.
    echo Access the application:
    echo   Backend API: http://localhost:8000
    echo   API Docs:    http://localhost:8000/docs
    echo   Frontend:    http://localhost:8501
    exit /b 0
) else (
    echo [ERROR] %FAILED% check^(s^) failed. Review errors above.
    echo.
    echo Troubleshooting steps:
    echo 1. Check container logs: docker-compose logs backend frontend
    echo 2. Ensure services are fully started ^(may take 30-40 seconds^)
    echo 3. Verify Docker Desktop has sufficient resources
    echo 4. Try: docker-compose down -v ^&^& docker-compose up -d
    exit /b 1
)

endlocal
