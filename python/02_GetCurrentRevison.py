import subprocess
import os


# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# Info.txt 파일의 경로 설정
info_file_path = os.path.join(script_dir, "..\Data\Info.txt")

# 파일에서 SVN 경로 읽기
try:
    with open(info_file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        svn_repo_path = None

        for line in lines:
            if line.startswith("SVN : "):
                svn_repo_path = line.split("SVN : ")[1].strip()
                break

        if svn_repo_path:
            print(f"특정 폴더의 경로: {svn_repo_path}")
        else:
            print("SVN 경로를 Info.txt 파일에서 찾을 수 없습니다.")

except FileNotFoundError:
    print(f"{info_file_path} 파일을 찾을 수 없습니다.")
    
# output 폴더 경로 설정
output_folder_path = os.path.join(script_dir, "../output")

# output 폴더가 없으면 생성
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 저장할 파일의 새로운 경로 설정
output_file_path = os.path.join(output_folder_path, "02_CurrentRevision.txt")

# 폴더로 이동
os.chdir(svn_repo_path)

# svn log 명령어 실행
try:
    result = subprocess.check_output(["svn", "log", "--limit", "1"], text=True)
    lines = result.splitlines()
    revision_info = None

    # svn log 출력에서 리비전 번호 찾기
    for line in lines:
        if line.startswith("r"):
            revision_info = line.strip()
            break

    if revision_info:
        revision_number = revision_info.split(" | ")[0][1:]  # "r"을 제외한 리비전 번호
        print(f"특정 폴더의 현재 리비전 번호: {revision_number}")

        # 리비전 번호를 파일로 저장
        with open(output_file_path, "w") as file:
            file.write(revision_number)
            #print(f"리비전 번호를 {output_file_path} 파일로 저장했습니다.")
    else:
        print("현재 리비전 정보를 찾을 수 없습니다.")

except FileNotFoundError:
    print("SVN 클라이언트가 설치되어 있지 않거나 경로가 올바르지 않습니다.")
except subprocess.CalledProcessError as e:
    print(f"오류 발생: {e}")
