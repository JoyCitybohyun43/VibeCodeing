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

# SVN 로그 명령어 실행하여 사용자 이름 가져오기
try:
    svn_log_command = ["svn", "log", "-r", revision_number, svn_path]
    result = subprocess.check_output(svn_log_command, text=True)
    lines = result.splitlines()
    
    # SVN 로그 출력에서 사용자 이름 찾기
    user_name = None
    for line in lines:
        if line.startswith("r" + revision_number + " | "):
            user_name = line.split("|")[1].strip()
            break

    if user_name:
        # 사용자 이름을 output 폴더의 04_UserName.txt에 저장
        user_name_file_path = os.path.join(script_dir, "../output", "04_UserName.txt")
        with open(user_name_file_path, "w") as file:
            file.write(user_name)
        print(f"사용자 이름 '{user_name}'가 {user_name_file_path}에 저장되었습니다.")
    else:
        print("사용자 이름을 찾을 수 없습니다.")

except subprocess.CalledProcessError as e:
    print(f"SVN 로그 명령어 실행 중 오류 발생: {e}")
except FileNotFoundError:
    print("SVN 클라이언트가 설치되어 있지 않거나 경로가 올바르지 않습니다.")
