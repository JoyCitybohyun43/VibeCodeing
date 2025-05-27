import subprocess
import os

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# info.txt 파일에서 SVN 경로 읽기
info_file_path = os.path.join(script_dir, "..\Data\info.txt")
try:
    with open(info_file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        svn_path = None
        for line in lines:
            if line.startswith("SVN : "):
                svn_path = line.split("SVN : ")[1].strip()
                break
        if not svn_path:
            raise ValueError("SVN 경로를 찾을 수 없습니다.")
except FileNotFoundError:
    print(f"{info_file_path} 파일을 찾을 수 없습니다.")
    exit()
except ValueError as e:
    print(e)
    exit()

# output/03_NextRevision.txt에서 리비전 번호 읽기
next_revision_file_path = os.path.join(script_dir, "../output", "01_NextRevision.txt")
try:
    with open(next_revision_file_path, "r") as file:
        revision_number = file.read().strip()
except FileNotFoundError:
    print(f"{next_revision_file_path} 파일을 찾을 수 없습니다.")
    exit()

# SVN 업데이트 명령 실행
try:
    subprocess.check_call(["svn", "update", "-r", revision_number, svn_path])
    print(f"SVN이 리비전 {revision_number}으로 업데이트 되었습니다.")
except subprocess.CalledProcessError as e:
    print(f"SVN 업데이트 명령어 실행 중 오류 발생: {e}")
