cd /d %~dp0

REM 최신 원격 변경 사항 가져오기
git pull origin main

REM 변경된 파일 모두 추가
git add .

REM 커밋 (변경 사항 없으면 건너뜀)
git diff --cached --quiet || git commit -m "Auto sync update"

REM 푸시
git push origin main

echo Auto sync complete.
pause