cd /d %~dp0

REM 민감 정보가 포함된 마지막 2개 커밋 완전 제거

git reset --hard HEAD~2

REM 민감 파일 재추적 방지
(echo GitInitAndPush.bat>>.gitignore)
(echo GitSetRemoteHTTPS.bat>>.gitignore)

REM 필요한 파일만 다시 추가 및 커밋
git add .
git commit -m "Clean commit without secrets"

git push -u origin main

echo Push complete.
pause