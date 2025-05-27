@echo off
cd /d %~dp0
git add .
git commit -m "Auto-commit: Add hello.py"
git push origin main