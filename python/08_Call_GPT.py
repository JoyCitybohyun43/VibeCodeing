# -*- coding: utf-8 -*-

import os
from openai import OpenAI

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# Info.txt 파일의 경로 설정
info_file_path = os.path.join(script_dir, "../Data/Info.txt")

# Respone 폴더 경로 설정
response_folder_path = os.path.join(script_dir, "../output/Respone")

# 파일을 읽어 API 키 설정
try:
    with open(info_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("api_key:"):
                api_key = line.split(":")[1].strip()
                break
    print("API 키 설정 완료:")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
except IndexError:
    print("올바른 형식의 API 키가 파일에 저장되어 있지 않습니다.")

# OpenAI API 키 설정
#openai.api_key = api_key
client = OpenAI(
    # This is the default and can be omitted
    #api_key=os.environ.get(api_key),
    api_key=api_key,
)

# output/FunctionInfo 폴더의 경로
folder_path = os.path.join(script_dir, "../output/FunctionInfo")

# 응답을 저장할 파일 경로 설정
output_file_path = os.path.join(script_dir, "../output/08_response.txt")

# 폴더 내의 파일 목록 가져오기
file_list = os.listdir(folder_path)

# 파일 내용 읽기 함수
def read_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        # utf-8로 디코딩 실패 시 다른 인코딩 사용
        with open(file_path, 'r', encoding='cp949') as file:
            return file.read()

# 파일별로 처리
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    code = read_file(file_path)
    
    print(" GPT 응답 대기중 ... ")
   
    # ChatCompletion을 사용하여 코드 취약점 파악
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """1.Answer in Korean, 2.C# code, Make sure this code checks for null properly. 3.Check whether a null exception can occur. 4. Singleton and .Instance are excluded from inspection 5. If there is no problem with the original code, not the modified code, “[No problem] output”. """},
            {"role": "user", "content": code}
        ]
    )

    # 지정된 폴더가 없으면 생성
    if not os.path.exists(response_folder_path):
        os.makedirs(response_folder_path)
    
    # 각 파일명으로 응답 저장
    response_file_path = os.path.join(response_folder_path, file_name)
    with open(response_file_path, 'w', encoding='utf-8') as response_file:
        response_file.write(f"[[[ {file_name} ]]]\n")
        response_file.write(response.choices[0].message.content)

print("각 파일에 대한 응답이 저장되었습니다.")
