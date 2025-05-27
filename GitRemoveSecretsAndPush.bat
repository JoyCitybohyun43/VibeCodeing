cd /d %~dp0

REM 토큰 포함된 배치 파일 Git에서 제거 (실제 파일은 삭제 안 됨)
git rm --cached GitInitAndPush.bat
git rm --cached GitSetRemoteHTTPS.bat

REM 변경 커밋
git commit -m "Remove token-exposed files"

REM 안전하게 푸시
git push origin main

echo Push complete.
pause