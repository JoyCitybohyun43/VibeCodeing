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

# save_class 함수 정의
def save_class(class_name, line_number, class_lines):
    output_file_name = f"{class_name}_{line_number}.cs"
    output_file_path = os.path.join(func_folder_path, output_file_name)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:  # UTF-8 인코딩으로 파일을 열기
        for line in class_lines:
            f.write(line)
            

# main 함수 정의
def main(input_file, req_line_number):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(input_file, 'r', encoding='cp949') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            print(f"{input_file} 파일의 인코딩을 확인할 수 없습니다.")
            return

    bracket_count = 0
    class_name = None
    class_lines = []
    preline = ""
    funclinenumber = 0
    #print(" test : ", lines)
    for line_number, line in enumerate(lines):
        # [클래스 및 함수 처리 로직]
        if "class" in line:
            class_index = line.find("class")  # "class" 문자열의 인덱스를 찾음
            if class_index != -1:
                first_space_index = line.find(" ", class_index)  # "class" 다음 공백 문자의 인덱스를 찾음
                second_space_index = line.find(" ", first_space_index + 1)  # 첫 번째 공백 다음 공백 문자의 인덱스를 찾음
                class_name = line[first_space_index + 1:second_space_index]  # 첫 번째 공백과 두 번째 공백 사이의 문자열을 추출
                class_name = class_name.strip()  # 문자열 양 끝의 공백을 제거
                #print(" test : ", class_name)
            bracket_count = 0
            class_lines = []
            continue

        if class_name:
            if bracket_count >= 2 :
                class_lines.append(line)
                
            for char in line:
                if char == '{':
                    bracket_count += 1
                    if bracket_count == 2 :
                        funclinenumber = line_number - 1
                        class_lines.append(preline)
                        class_lines.append(line)
                        if funclinenumber > req_line_number : 
                            return
                elif char == '}':
                    bracket_count -= 1
                    if bracket_count == 1 :
                        #print(" test : ", funclinenumber)
                        #print(" test : ", req_line_number)
                        #print(" test : ", line_number)
                        if funclinenumber <= req_line_number and req_line_number <= line_number :
                            save_class(class_name, funclinenumber, class_lines)
                            #print(" funclinenumber : ", funclinenumber)
                            #print(" line_number : ", line_number)
                        class_lines = []
            preline = line

# 파일에서 리비전 번호 읽기

try:
    try:
        with open(revision_file_path, "r", encoding='utf-8') as file:
            change_string = file.read().strip()
    except UnicodeDecodeError:
        with open(revision_file_path, "r", encoding='cp949') as file:
            change_string = file.read().strip()
except FileNotFoundError:
    print(f"{revision_file_path} 파일을 찾을 수 없습니다.")
    exit()



# 정규 표현식을 사용하여 각 Index 및 수정된 라인 번호를 추출
index_pattern = r'Index:\s+([^\n]+)'
pattern = r'@@\s+\-\d+,\d+\s+\+(\d+),\d+\s+@@'

# 결과를 저장할 리스트
results = []

# 각 Index 섹션을 분리 및 처리
index_sections = re.split(index_pattern, change_string)[1:]
for i in range(0, len(index_sections), 2):
    index_text = index_sections[i].strip()  # 인덱스 텍스트 추출 및 공백 제거
    section_content = index_sections[i + 1]  # 섹션 내용
    matches = re.findall(pattern, section_content)  # 패턴과 일치하는 모든 항목 찾기
    results.append(f"Index: {index_text}")  # 결과에 인덱스 텍스트 추가

    for match in matches:
        results.append(f"LINE : {match}")  # 결과에 일치하는 라인 추가
        start_line = int(match)  # 일치하는 항목을 정수로 변환하여 시작 라인으로 설정
        # 0이면 삭제되었다고 간주함
        if start_line == 0:  # 시작 라인이 0이면 함수를 반환하고 다음 반복으로 넘어감
            continue           

        main(index_text, start_line)  # main 함수 호출

