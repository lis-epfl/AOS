@echo off

REM ── 1) Ensure Mosquitto is fresh ────────────────────────────────────
cd "C:\Program Files\mosquitto"
net stop mosquitto
net start mosquitto

REM    Run Mosquitto in this same window (backgrounded)
start /B "" mosquitto -c mosquitto.conf

REM ── 2) Back to repo root ────────────────────────────────────────────
cd /d %~dp0

REM Start the executable file
start "" "AOS server\DroneSwarmServer.exe"

REM Open two HTML files
start "" "AOS waypoint planning\index.html"
start "" "AOS map visualization\AOS-Map.html"

