@echo off
echo Starting Driving Control Servers...
echo.
echo HTTPS Server: https://localhost:8000 (for mobile browsers)
echo HTTP Server:  http://localhost:8001 (for Roblox)
echo.
echo Both servers share the same variables - no more sync issues!
echo Press Ctrl+C to stop both servers
echo.

poetry run python launch_unified.py

pause
