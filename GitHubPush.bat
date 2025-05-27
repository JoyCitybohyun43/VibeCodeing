@echo off
cd /d %~dp0
git remote set-url origin git@github.com:JoyCitybohyun43/VibeCodeing.git
git add .
git commit -m "Auto-commit: Add hello.py"
git push origin main