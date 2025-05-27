import os
import shutil

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# Info.txt 파일의 경로 설정
info_file_path = os.path.join(script_dir, "..", "Data", "Info.txt")

# 파일의 기준 크기 설정
try:
    with open(info_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("MAX_FILE_SIZE :"):
                FileSize = line.split(":")[1].strip()
                # FileSize 값을 정수로 변환하고 KB 단위로 환산
                MAX_FILE_SIZE = int(FileSize) * 1024  # KB 단위로 변환
                break
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    MAX_FILE_SIZE = 10 * 1024  # 기본값 설정: 10KB
except ValueError:
    print("MAX_FILE_SIZE 값이 올바른 숫자 형식이 아닙니다.")
    MAX_FILE_SIZE = 10 * 1024  # 기본값 설정: 10KB
except IndexError:
    print("올바른 형식의 MAX_FILE_SIZE 키가 파일에 저장되어 있지 않습니다.")
    MAX_FILE_SIZE = 10 * 1024  # 기본값 설정: 10KB

# 원본 폴더와 대상 폴더 경로 설정
source_folder = os.path.join(script_dir, "..", "output", "FunctionInfo")
target_folder = os.path.join(script_dir, "..", "output", "FileSizeOver")

# 대상 폴더가 없으면 생성
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 원본 폴더 내의 모든 파일을 순회
for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)

    # 파일 크기가 설정값 이상인지 확인
    if os.path.getsize(file_path) >= MAX_FILE_SIZE:
        # 파일을 대상 폴더로 이동
        shutil.move(file_path, os.path.join(target_folder, file_name))
        print(f"이동됨: {file_name}")
