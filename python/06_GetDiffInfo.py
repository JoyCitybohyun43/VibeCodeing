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
    
# 03_NextRevision.txt 파일의 경로 설정
revision_file_path = os.path.join(script_dir, "..\\output\\01_NextRevision.txt")

# 파일에서 리비전 번호 읽기
try:
    with open(revision_file_path, "r") as file:
        specific_revision = file.read().strip()
except FileNotFoundError:
    print(f"{revision_file_path} 파일을 찾을 수 없습니다.")
    exit()

# SVN diff 명령어 실행 및 결과 처리
try:
    result_bytes = subprocess.check_output(["svn", "diff", "-c", specific_revision, svn_repo_path])

    result = None
    for encoding in ['utf-8', 'cp949', 'iso-8859-1']:
        try:
            result = result_bytes.decode(encoding)
            break  # 성공적으로 디코딩하면 반복 중단
        except UnicodeDecodeError:
            continue  # 현재 인코딩에서 실패하면 다음 인코딩으로 넘어감

    if result is None:
        raise UnicodeDecodeError("모든 인코딩에서 디코딩에 실패했습니다.")

    # 성공적으로 디코딩되면 결과를 파일로 저장
    with open(os.path.join(script_dir, "..\\output\\06_DiffInfo.txt"), "w", encoding='utf-8') as output_file:
        output_file.write(result)
        print("결과를 06_DiffInfo.txt 파일로 저장했습니다.")

except FileNotFoundError:
    print("SVN 클라이언트가 설치되어 있지 않거나 경로가 올바르지 않습니다.")
except subprocess.CalledProcessError as e:
    print(f"오류 발생: {e}")
