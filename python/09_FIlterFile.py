import os
import re
import glob
import shutil
    
    
def filter_and_save_files():
    # 파일을 필터링할 단어
    file_filter_strings_groups = [
            ["코드","이미 적절한 널 체크가 존재"],
            ["코드","이미 처리되어 있는"],
            ["제공된 코드 기준", "올바르게 적용되어"],
            ["널 포인트 체크가 필요 없어"],
            ["정상적으로 작동할 것으로 예상"],
            ["코드","올바르게 적용"],
            ["코드","널 포인트 체크가 필요 없어"],
            ["코드","정상적으로 작동할 것으로 예상"],
            ["코드","null 포인터 체크", "필요한 부분" , "존재하지 않습니다"],
            ["결론적으로","관찰되지 않았습니다"],
            ["코드","명시적으로" , "보이지 않습니다"],
            ["정상적으로 작동할 것으로 보입니다."],
            ["코드" , "체크", "필요", "없는"],
            ["코드" , "이미", "체크"],
            ["코드" , "이미", "체크"],
            ["코드" , "체크", "보이지", "않습"],
           
            # 여기에 추가 그룹을 계속 추가할 수 있습니다.
    ]
    # 원본 파일이 위치한 폴더 경로
    source_folder = os.path.join(os.path.dirname(__file__), "../output/Respone")
    # 저장할 폴더 경로
    target_folder = os.path.join(os.path.dirname(__file__), "../output/FilterFile")
    # 필터 결과를 저장할 폴더 경로
    filter_result_folder = os.path.join(os.path.dirname(__file__), "../output/FilterFileResult")

    # 해당 폴더 내의 모든 파일 경로를 가져옴
    file_paths = glob.glob(os.path.join(source_folder, "*"))  # 이 라인을 추가함


    # 필터 결과 폴더가 없으면 생성
    if not os.path.exists(filter_result_folder):
        os.makedirs(filter_result_folder)

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # 한 라인에 필터링 단어가 두 개 이상 나오는지 확인
                skip_file = False
                found_words_summary = ""  # 필터된 단어 요약 문자열 초기화
                for line in lines:
                    for group in file_filter_strings_groups:
                        if all(word in line for word in group):
                            skip_file = True
                            found_groups_summary = ', '.join(group)  # 필터된 그룹 요약
                            break  # 하나의 그룹이 만족하면 나머지 그룹은 검사하지 않고 루프 탈출
                    if skip_file:
                        break
                if not skip_file:
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    shutil.copy(file_path, os.path.join(target_folder, os.path.basename(file_path)))
                else:
                    result_file_path = os.path.join(filter_result_folder, os.path.basename(file_path))
                    with open(result_file_path, 'w', encoding='utf-8') as result_file:
                        result_file.write(f"Filter: {found_groups_summary}\n\n")
                        result_file.writelines(lines)
        except Exception as e:
            print(f"파일 처리 오류 ({file_path}): {e}")

# 함수 호출
filter_and_save_files()
