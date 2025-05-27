import os
import re

def read_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        # 파일이 없는 경우 None 반환
        return None
    except UnicodeDecodeError:
        # utf-8 인코딩으로 읽기 실패 시 cp949 인코딩으로 시도
        try:
            with open(file_path, 'r', encoding='cp949') as file:
                return file.read()
        except UnicodeDecodeError:
            return None
            
            
def add_function_info(input_path, output_path, function_info_folder):
    # 08_response.txt 파일 읽기
    content = read_file(input_path)
    
    # 파일 내용이 없을 경우 새 파일 생성
    if content is None:
        print(f"파일 '{input_path}'이(가) 존재하지 않습니다. 새 파일을 생성합니다.")
        # 빈 파일 생성
        open(input_path, 'w', encoding='utf-8').close()
        content = ""  # 내용을 빈 문자열로 설정

    # [[[ ]]]로 둘러싸인 부분 찾기
    pattern = r'\[\[\[ (.*?) \]\]\]'
    file_names = re.findall(pattern, content)

    for file_name in file_names:
        # functionInfo 폴더에서 파일 찾기
        function_info_path = os.path.join(function_info_folder, file_name)
        if not os.path.exists(function_info_path):
            print(f"파일 '{function_info_path}'을(를) 찾을 수 없습니다. 다음 파일로 넘어갑니다.")
            continue  # 파일이 없으면 이번 반복을 건너뛰고 다음 파일로 넘어감

        if os.path.exists(function_info_path):
            function_content = read_file(function_info_path)
            first_line = function_content.splitlines()[0] if function_content else ""

            # 파일 이름에서 마지막 "_"를 찾아 File과 Line으로 분리
            last_underscore_index = file_name.rfind('_')
            if last_underscore_index != -1:
                file_info = file_name[:last_underscore_index]
                line_info = file_name[last_underscore_index + 1:-3]  # ".cs"를 지우기 위해 마지막 3글자 제거
                content = content.replace(f'[[[ {file_name} ]]]', f'[[[ {file_name} ]]]\nFile : {file_info}\nLine : {line_info}\n\n{first_line}\n')
            else:
                content = content.replace(f'[[[ {file_name} ]]]', f'[[[ {file_name} ]]]\nFile : \nLine : \n\n{first_line}\n')
        else:
            print(f"파일 '{function_info_path}'을(를) 찾을 수 없습니다.")

    # 변경된 내용을 09_ResponseAddFunc.txt에 저장
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"파일이 '{output_path}'에 저장되었습니다.")

# 파일 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(script_dir, "../output", "08_response.txt")
output_file_path = os.path.join(script_dir, "../output", "09_ResponseAddFunc.txt")
function_info_folder_path = os.path.join(script_dir, "../output", "functionInfo")

# 함수 실행
add_function_info(input_file_path, output_file_path, function_info_folder_path)
