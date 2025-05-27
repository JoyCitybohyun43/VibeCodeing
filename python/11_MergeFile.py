import os
import re

def add_function_and_save():
    # 입력 폴더와 최종 출력 파일의 경로 설정
    input_folder = os.path.join(os.path.dirname(__file__), "../output/filterline")
    output_file_path = os.path.join(os.path.dirname(__file__), "../output/08_response.txt")

    # 입력 폴더 내의 모든 파일 목록 가져오기
    file_list = os.listdir(input_folder)

    # 파일 목록이 비어있지 않은 경우에만 처리
    if file_list:
        # 최종 출력 파일에 저장할 내용을 담을 리스트 초기화
        content_list = []

        # 입력 폴더 내의 모든 파일 처리
        for file_name in file_list:
            input_file_path = os.path.join(input_folder, file_name)

            # 파일을 열고 내용 읽기
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # 파일 내용의 공백, 줄바꿈, 탭 등을 제거
                stripped_content = re.sub(r'\s+', '', content)

                # 공백 제거 후 내용이 "[[["로 시작하고 "]]]"로 끝나는지 확인
                if stripped_content.startswith("[[[") and stripped_content.endswith("]]]"):
                    continue  # 이 조건을 만족하면 파일 내용을 추가하지 않고 다음 파일로 넘어감

                #print(stripped_content+ "\n\n")
                
                # 파일 내용을 리스트에 추가
                content_list.append(content)

        # 모든 파일의 내용을 \n\n로 구분하여 하나의 문자열로 합치기
        final_content = '\n\n'.join(content_list)

        # 최종 결과를 출력 파일에 저장
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(final_content)

        print("파일 저장이 완료되었습니다.")
    else:
        print("입력 폴더에 파일이 없어서 파일 저장을 하지 않습니다.")

# 함수 호출
add_function_and_save()
