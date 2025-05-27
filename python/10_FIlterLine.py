import os

# 입력 폴더와 출력 폴더의 상대 경로 설정
input_folder = os.path.join(os.path.dirname(__file__), "../output/FilterFile")
output_folder = os.path.join(os.path.dirname(__file__), "../output/FilterLine")
filter_line_result_folder = os.path.join(os.path.dirname(__file__), "../output/FilterLineResult")

# 라인을 필터링할 단어	
line_filter_strings_groups = [
    ["참조 예외", "가능성은 없습니다"],
    ["참조", "없습니다"],
    ["고려 대상", "제외"],
    ["예외", "발생하지 않습니다"],
    ["문제", "발생하지 않습니다"],
    ["예외가 발생할 가능성", "우려할 필요는 없어"],
    ["걱정할 필요", "없습니다"],
    ["분석 대상", "제외"],
    ["발생할 가능성", "없습"],
    ["처리 대상", "제외"],
    ["인스턴스", "제외"],
    ["싱글턴", "예외"],
    ["Instance", "위험은 없습니다."],
    ["Instance", "싱글톤"],
    ["Instance", "`null`인 경우"],
    ["Instance", "`null`", "수행하지 않"],
    ["이 부분은", "예외를" , "발생시키지" , "않을"],
    ["참조 예외는 발생하지 않아"],
    ["null인 경우에 대한 예외는 없습니다."],
    ["이 경우에 대해서도","검사하여 처리하고 있습니다"],
    ["참조 예외가 발생하는 것을 방지합니다"],
    ["다만" , "참조 예외를 방지합니다"],
    ["참조 예외를 방지하는 로직이 이미 포함되어 있습니다"],
    ["확실하게 말하기 어렵습니다."],
    ["클래스 내 다른 곳에서 초기화될 가능성이 높습니다"],
    ["필요한 부분이 나타나지 않습니다."],
	["판단하기 어렵습니다"],
    ["문제를 찾지 못"],
    ["이미", "적절","처리"],
    ["체크가 필요한 부분" , "직접적으로 보이지 않습니다"],
    ["문제가 없어 보입니다."],
    ["문제가 없으므로"],
    ["적절히 처리하고 있습니다"],
    ["적절히 포함되어 있습니다."],
    ["적절하게 처리하고 있습니다"],
    ["적절히 확인하고 있습니다"],
    ["문제가 없는 것으로"],
    ["적절히 이루어지고"],
    ["적절히 수행하고"],
    ["[No problem]"],
    ["[문제 없음]"],



    
    # 여기에 추가 그룹을 계속 추가할 수 있습니다.
]	

# 출력 폴더와 필터링된 내용을 저장할 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(filter_line_result_folder):
    os.makedirs(filter_line_result_folder)
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
    
    
# 입력 폴더 내의 모든 파일 처리
file_names = os.listdir(input_folder)
if file_names:  # 파일 목록이 비어있지 않은 경우에만 처리
    for file_name in file_names:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)
        filter_line_result_file_path = os.path.join(filter_line_result_folder, file_name)

        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file, \
            open(filter_line_result_file_path, 'w', encoding='utf-8') as filter_line_result_file:

            skip_lines = False  # 조건에 만족하는 다음 라인을 찾을 때까지 건너뛰기 위한 플래그

            for line in input_file:
                if skip_lines:
                    skip_lines = False
                    continue

                for group in line_filter_strings_groups:
                    if all(word in line for word in group):
                        filter_line_result_file.write("Filter: " + " & ".join(group) + "\n" + line)
                        skip_lines = True
                        break
                else:
                    output_file.write(line)
else:
    print(f"'{input_folder}' 폴더에 파일이 없습니다. 처리를 건너뜁니다.")

print("10_FIlterLine.py 작업이 완료되었습니다.")
