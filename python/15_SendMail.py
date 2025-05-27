import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# 이메일 설정 변수 초기화
sending_server = "smtp.joycity.com"
to_emails = []
from_address = ""
message_subject = ""

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# 04_UserName.txt 파일의 경로 설정 및 사용자 이름 읽기
user_name_file_path = os.path.join(script_dir, "../output", "04_UserName.txt")
try:
    with open(user_name_file_path, 'r', encoding='utf-8') as file:
        user_name = file.read().strip()
except FileNotFoundError:
    print(f"파일 '{user_name_file_path}'을(를) 찾을 수 없습니다.")
    exit()

# Info.txt 파일의 경로 설정
info_file_path = os.path.join(script_dir, "../Data/", "Info.txt")


# Info.txt 파일의 경로 설정 및 이메일 설정 값 할당
try:
    with open(info_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 공백 및 줄 바꿈 문자 제거
            if line.startswith("to_email"):
                email = line.split(":")[1].strip()
                if email not in to_emails:  # 중복 방지를 위한 검사
                    to_emails.append(email)  # Info.txt에서 기본 수신자 추가
            elif line.startswith("to_email1"):
                email = line.split(":")[1].strip()
                if email not in to_emails:  # 중복 방지를 위한 검사
                    to_emails.append(email)  # Info.txt에서 람님 추가
            elif line.startswith("from_address"):
                from_address = line.split(":")[1].strip()
                # from_address가 to_emails에 이미 존재하는지 확인 후 추가
                if from_address not in to_emails:
                    # 이 경우에는 from_address를 to_emails에 추가하지 않음
                    pass
            elif line.startswith("message_subject"):
                message_subject = line.split(":")[1].strip()
            elif user_name in line:
                email = line.split(":")[1].strip()
                if email not in to_emails:  # 중복 방지를 위한 검사
                    to_emails.append(email)  # 04_UserName.txt에서 읽은 사용자 이메일 추가
except FileNotFoundError:
    print(f"파일 '{info_file_path}'을(를) 찾을 수 없습니다.")
    exit()
# bohyun43@joycity.com 추가
# to_emails.append("bohyun43@joycity.com")

# 설정값 출력 (디버깅용)
print("수신 이메일 주소:", to_emails)
print("보내는 이메일 주소:", from_address)
print("이메일 제목:", message_subject)

# 현재 스크립트의 경로를 기반으로 HTML 파일 경로 설정
html_file_path = os.path.join(script_dir, "../output", "11_highlighted_text.html")

# HTML 파일 읽기
try:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        message_body = file.read()
except FileNotFoundError:
    print(f"파일 '{html_file_path}'을(를) 찾을 수 없습니다.")
    exit()

# MIME 메시지 생성
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = ", ".join(to_emails)  # 이메일 주소 리스트를 문자열로 변환
msg['Subject'] = message_subject

# 메시지 본문 첨부
msg.attach(MIMEText(message_body, 'html'))

# SMTP 서버를 통해 이메일 전송
try:
    with smtplib.SMTP(sending_server, 25) as server:
        server.sendmail(from_address, to_emails, msg.as_string())
    print("이메일이 성공적으로 전송되었습니다.")
except Exception as e:
    print(f"이메일 전송 중 오류가 발생했습니다: {e}")
