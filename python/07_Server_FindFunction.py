import re
import os
import sys

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# 06_DiffInfo.txt 파일의 경로 설정
revision_file_path = os.path.join(script_dir,"..\\output\\06_DiffInfo.txt")

# Func 폴더 경로 설정
func_folder_path = os.path.join(script_dir, "..\\output\\FunctionInfo")

# FunctionInfo 폴더가 없으면 생성
if not os.path.exists(func_folder_path):
    os.makedirs(func_folder_path)
    print(f"'{func_folder_path}' 폴더가 생성되었습니다.")


# 파일에서 리비전 번호 및 수정된 라인 번호 읽기
try:
    with open(revision_file_path, "r", encoding='utf-8') as file:
        change_string = file.read().strip()
        #print(f"{change_string} change_string.")
except UnicodeDecodeError:
    try:
        with open(revision_file_path, "r", encoding='cp949') as file:
            change_string = file.read().strip()
            #print(f"{change_string} change_string.")
    except UnicodeDecodeError:
        print("파일 인코딩 오류")
except FileNotFoundError:
    print(f"{revision_file_path} 파일을 찾을 수 없습니다.")
    sys.exit()
    
    
def extract_functions_from_cpp(cpp_file_path, target_line_number):
    try:
        with open(cpp_file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        print(f"파일 '{cpp_file_path}'을(를) 읽는 도중 인코딩 문제가 발생했습니다.")
        return

    function_start = None
    function_end = None
    bracket_count = 0
    function_lines = []

    for i, line in enumerate(lines):
        if '{' in line:
            bracket_count += line.count('{')
            if bracket_count == 1 and function_start is None:
                function_start = i - 1
        if '}' in line:
            bracket_count -= line.count('}')
            if bracket_count == 0 and function_start is not None:
                function_end = i
                if function_start < target_line_number <= function_end:
                    function_lines = lines[function_start:function_end + 1]
                    break
                else:
                    function_start = None

    if function_lines:
        base_name = os.path.basename(cpp_file_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        output_file_name = f"{file_name_without_ext}_{target_line_number}.cpp"
        output_file_path = os.path.join(func_folder_path, output_file_name)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:  # UTF-8 인코딩으로 파일 쓰기
            output_file.writelines(function_lines)
        print(f"Function containing line {target_line_number} has been saved to {output_file_path}")
    else:
        print(f"No function containing line {target_line_number} was found.")



        
# 정규 표현식을 사용하여 각 Index 및 수정된 라인 번호를 추출
index_pattern = r'Index:\s+([^\n]+)'
pattern = r'@@\s+\-\d+,\d+\s+\+(\d+),\d+\s+@@'



index_sections = re.split(index_pattern, change_string)[1:]
for i in range(0, len(index_sections), 2):
    index_text = index_sections[i].strip()
    if index_text.endswith('.h'):  # .h 파일 확장자로 끝나는 경우 스킵
        print(f"'{index_text}'는 .h 파일이므로 스킵됩니다.")
        continue  # .h 파일은 처리하지 않고 다음 반복으로 넘어감

    section_content = index_sections[i + 1]
    matches = re.findall(pattern, section_content)
    print(f"처리 중인 파일: {index_text}")  # 로그 추가

    for match in matches:
        start_line = int(match)
        print(f"변경된 라인 번호: {start_line}")  # 로그 추가
        extract_functions_from_cpp(index_text, start_line)
        
        
        
