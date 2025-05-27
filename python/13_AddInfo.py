import os

def add_function_and_save():
    # 기본 파일 및 폴더 경로 설정
    base_file_path = os.path.join(os.path.dirname(__file__), "../output/09_ResponseAddFunc.txt")    
    Next_Revision_file_path = os.path.join(os.path.dirname(__file__), "../output/01_NextRevision.txt")
    response_folder = os.path.join(os.path.dirname(__file__), "../output/Respone")
    function_info_folder = os.path.join(os.path.dirname(__file__), "../output/FunctionInfo")  # FunctionInfo 폴더 경로 추가
    filter_file_result_folder = os.path.join(os.path.dirname(__file__), "../output/FilterFileResult")
    filter_line_result_folder = os.path.join(os.path.dirname(__file__), "../output/FilterLineResult")
    result_file_path = os.path.join(os.path.dirname(__file__), "../output/10_ResultData.txt")
    Log_file_path = os.path.join(os.path.dirname(__file__), "../Logs/ConsoleLog.txt")
    # 결과 파일 생성 및 쓰기 시작
    with open(result_file_path, 'w', encoding='utf-8') as result_file:

        # "Review" 문자열의 전체 길이를 계산 (양쪽 공백 포함)
        total_length = 150


        result_file.write("\n" + "-" * total_length + "\n")
        review_text = "[ Review ]"
        padding_length = (total_length - len(review_text)) // 2  # "Review" 문자열 양쪽에 채울 공백의 길이
        result_file.write(' ' * padding_length + review_text + "\n")
        result_file.write("-" * total_length + "\n")
        
        # 리비전 정보 추가
        if os.path.exists(Next_Revision_file_path):
            with open(Next_Revision_file_path, 'r', encoding='utf-8') as Revisionbase_file:
                result_file.write("\n" + "Revision : " + Revisionbase_file.read() + "\n")
        result_file.write("\n" + "\n")
        
        # 기본 파일 내용 추가
        if os.path.exists(base_file_path):
            with open(base_file_path, 'r', encoding='utf-8', errors='ignore') as base_file:
                result_file.write(base_file.read() + "\n")
        else:
            # base_file_path 파일이 없는 경우 "Good"이라고만 기록
            result_file.write(" Good \n")

        result_file.write("\n" + "\n"+ "\n"+ "\n")
        
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        result_file.write("[ 이 아래는 안 봐도 됨요 ]" + "\n")
        
        result_file.write("\n" + "-" * total_length + "\n")
        review_text = "[ Log ]"
        padding_length = (total_length - len(review_text)) // 2  
        result_file.write(' ' * padding_length + review_text + "\n")
        result_file.write("-" * total_length + "\n")
        
        
        result_file.write("\n" + "-" * total_length + "\n")
        result_file.write(' ' * padding_length + "[ Function ]" + "\n")
        result_file.write("-" * total_length + "\n")
        
        # FunctionInfo 폴더의 파일 내용 추가
        for file_name in os.listdir(function_info_folder):
            file_path = os.path.join(function_info_folder, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                result_file.write("\n```csharp\n")
                result_file.write(file.read() + "\n")
                result_file.write("```\n\n")

        #result_file.write("\n[Respone]\n\n")

        result_file.write("\n" + "-" * total_length + "\n")
        result_file.write(' ' * padding_length + "[ 응답 원본 ]" + "\n")
        result_file.write("-" * total_length + "\n")
        # Respone 폴더의 파일 내용 추가
        for file_name in os.listdir(response_folder):
            file_path = os.path.join(response_folder, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                result_file.write(file.read() + "\n")

        #result_file.write("\n[FilterFileResult] : 필터된 파일\n\n")

        result_file.write("\n" + "-" * total_length + "\n")
        result_file.write(' ' * padding_length + "[ 파일 필터링 ]" + "\n")
        result_file.write("-" * total_length + "\n")
        # FilterFileResult 폴더의 파일 내용 추가
        for file_name in os.listdir(filter_file_result_folder):
            file_path = os.path.join(filter_file_result_folder, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                result_file.write(file.read() + "\n")

        #result_file.write("\n[FilterLineResult] : 필터된 라인\n\n")


        result_file.write("\n" + "-" * total_length + "\n")
        result_file.write(' ' * padding_length + "[ 라인 필터링 ]" + "\n")
        result_file.write("-" * total_length + "\n")
        # FilterLineResult 폴더의 파일 내용 추가
        for file_name in os.listdir(filter_line_result_folder):
            file_path = os.path.join(filter_line_result_folder, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                result_file.write(file.read() + "\n")
                
                
                
        result_file.write("\n" + "-" * total_length + "\n")
        result_file.write(' ' * padding_length + "[ Process Log ]" + "\n")
        result_file.write("-" * total_length + "\n")               
        if os.path.exists(Log_file_path):
            with open(Log_file_path, 'r', encoding='utf-8', errors='ignore') as base_file:
                result_file.write(base_file.read() + "\n")


    print("작업이 완료되었습니다.")

# 함수 호출
add_function_and_save()
