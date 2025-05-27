import os
import shutil

# 현재 스크립트의 디렉터리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# 삭제할 폴더의 경로 설정
output_folder_path = os.path.join(script_dir, "../output")

# 백업 폴더의 경로 설정
backup_folder_path = os.path.join(script_dir, "../backup")

# '10_highlighted_text.html' 파일 확인 후 복사
highlighted_text_file_path = os.path.join(output_folder_path, "11_highlighted_text.html")

if os.path.exists(highlighted_text_file_path):
    # '01_NextRevision.txt' 파일 읽기
    current_revision_file_path = os.path.join(output_folder_path, "01_NextRevision.txt")
    
    if os.path.exists(current_revision_file_path):
        with open(current_revision_file_path, 'r') as file:
            folder_name = file.read().strip()  # 파일 내용을 읽어와서 앞뒤 공백을 제거하여 폴더 이름으로 사용

        # '../backup' 폴더로 'output' 폴더 복사
        backup_folder_path = os.path.join(script_dir, "../backup", folder_name)
        
        if os.path.exists(backup_folder_path):
            print(f"'{backup_folder_path}' 폴더가 이미 존재합니다.")
        else:
            shutil.copytree(output_folder_path, backup_folder_path)
            print(f"'output' 폴더를 '{backup_folder_path}'로 복사하였습니다.")
    else:
        print(f"'01_NextRevision.txt' 파일이 'output' 폴더 내에 존재하지 않습니다.")
else:
    print(f"'10_highlighted_text.html' 파일이 'output' 폴더 내에 존재하지 않아 복사 작업이 수행되지 않습니다.")


# 폴더가 존재하는지 확인하고, 존재하면 안전하게 삭제
if os.path.exists(output_folder_path):
    # 폴더 내의 모든 파일과 하위 디렉터리를 삭제
    for root, dirs, files in os.walk(output_folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)
    
    # 이제 빈 폴더를 삭제할 수 있음
    os.rmdir(output_folder_path)
    print(f"'{output_folder_path}' 폴더가 삭제되었습니다.")
else:
    print(f"'{output_folder_path}' 폴더가 존재하지 않습니다.")
