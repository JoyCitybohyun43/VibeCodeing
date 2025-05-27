@echo off
cd /d %~dp0

:: SSH 키 생성
ssh-keygen -t rsa -b 4096 -C "bohyun43@naver.com" -f "%userprofile%\.ssh\id_rsa" -N ""

:: SSH 에이전트 시작
powershell -Command "Start-Service ssh-agent"

:: SSH 키 추가
ssh-add %userprofile%\.ssh\id_rsa

:: 공개 키 복사 (클립보드)
powershell -Command "Get-Content $env:USERPROFILE\.ssh\id_rsa.pub | Set-Clipboard"

@echo 공개키가 클립보드에 복사되었습니다.
@echo https://github.com/settings/ssh/new 에 접속해서 키를 등록하세요.
pause