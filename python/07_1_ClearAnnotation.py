import os
import re

def remove_comments_from_files(directory):
    # 주어진 디렉토리의 모든 파일을 순회
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # 파일 읽기 시도 (여러 인코딩으로 시도)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='cp949') as file:
                    content = file.read()
            except UnicodeDecodeError as e:
                print(f"{filename} 파일을 읽을 수 없습니다. 인코딩 문제: {e}")
                continue  # 다음 파일로 넘어감

        # 한 줄 주석과 여러 줄 주석 제거
        content_no_single_line_comments = re.sub(r'//.*', '', content)  # 한 줄 주석 제거
        content_no_comments = re.sub(r'/\*[\s\S]*?\*/', '', content_no_single_line_comments)  # 여러 줄 주석 제거

        # 변경된 내용으로 파일 다시 쓰기
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content_no_comments)

    print("모든 파일에서 주석이 제거되었습니다.")

def compress_empty_lines(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open(filepath, 'w', encoding='utf-8') as file:
                previous_line_empty = False
                for line in lines:
                    if line.strip() == "":
                        if not previous_line_empty:
                            file.write("\n")
                            previous_line_empty = True
                    else:
                        file.write(line)
                        previous_line_empty = False
        except UnicodeDecodeError as e:
            print(f"{filename} 파일 처리 중 오류 발생: {e}")

    print("모든 파일에서 연속된 빈 줄이 축소되었습니다.")
    
    
# 호출되는 같은 경로의 ../output/FunctionInfo/ 폴더
current_path = os.path.dirname(os.path.abspath(__file__))
function_info_folder = os.path.join(current_path, "../output/FunctionInfo")

# 주석 제거 함수 실행
remove_comments_from_files(function_info_folder)

# 주석 제거 후 연속된 빈 줄 축소 함수 실행
compress_empty_lines(function_info_folder)