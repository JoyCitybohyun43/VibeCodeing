import re
import os

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def apply_code_block_style(match):
    """```로 둘러싸인 코드 블록에 스타일을 적용합니다."""
    code_block = match.group(1)

    # 첫 줄과 나머지 줄 분리
    first_line, *rest_of_lines = code_block.split('\n', 1)

    # C# 코드에 대한 렉서를 가져옵니다.
    lexer = get_lexer_by_name("csharp")

    # HTML 포맷터를 생성합니다.
    formatter = HtmlFormatter(style="monokai")

    # 나머지 줄에 대해 스타일 적용
    rest_styled = highlight('\n'.join(rest_of_lines), lexer, formatter) if rest_of_lines else ''

    # 첫 줄에 회색 배경 적용 및 나머지 스타일링된 코드와 결합
    styled_code_block = f'<pre style="background-color: #5c5858;">{first_line}</pre>{rest_styled}'

    return styled_code_block
def apply_custom_bold_style_Red(text):
    """'null 참조 예외', 'null', 'null인', 'null일', 'NullReferenceException이', 'NullReferenceException'이 포함된 텍스트를 빨간색으로 변경하되, ``` 와 ``` 사이는 변경하지 않습니다."""

    def replace_red(match):
        # ``` 와 ``` 사이의 텍스트는 변경하지 않음
        if match.group(1):
            return match.group(0)
        # 그 외의 경우 빨간색으로 변경
        else:
            return f"<span style='color: #d44242;'>{match.group(2)}</span>"

    # ``` 와 ``` 사이의 텍스트와 지정된 단어들을 찾는 정규 표현식
    pattern = r"(```[\s\S]*?```)|(null 참조 예외|\bnull\b|\bnull인\b|\bnull일\b|NullReferenceException이|NullReferenceException)"
    text = re.sub(pattern, replace_red, text)

    return text

    
    
def apply_custom_bold_style(text):
    """'File :' 또는 'Line :'이 포함된 라인의 텍스트를 볼드 처리하고 녹색으로 변경합니다."""
    # 라인별로 분리하여 각 라인을 검사하고 조건에 맞는 라인을 볼드 처리 및 녹색으로 변경
    lines = text.split('\n')
    styled_lines = [f"<span style='font-weight: bold; color: #04b806;'>{line}</span>" if "File :" in line or "Line :" in line else line for line in lines]
    

    return '\n'.join(styled_lines)

def apply_function_style(text):
    """함수 정의 라인에 CSS 스타일을 적용합니다."""
    styled_lines = []
    for line in text.split('\n'):
        # 함수 정의 패턴을 간단히 확인합니다. (예: 'void functionName(')
        if re.search(r'\b\w+\b \w+\(', line):
            # 함수 정의 라인에 스타일을 적용합니다.
            styled_line = f"<span style='color: #e5ff00;'>{line}</span>"
        else:
            styled_line = line
        styled_lines.append(styled_line)
    return '\n'.join(styled_lines)  
    
def apply_bold_style(text):
    """볼드 처리된 부분에 스타일을 적용합니다."""
    return re.sub(r'\[\[\[(.*?)\]\]\]', r'<b>\1</b>', text)

def apply_indent_style(text):
    """들여쓰기를 적용합니다."""
    def add_indent(match):
        indent_div = '<div style="margin-left: 20px;">'
        return f"{match.group(1)}{indent_div}{match.group(2).replace('<br>', '<br>' + ' ' * 4)}</div>{match.group(3)}"
    return re.sub(r'(<b>)(.*?)(</b>)', add_indent, text, flags=re.DOTALL)

def highlight_text(text, background_color, font_color):
    """주어진 텍스트에 HTML 스타일을 적용합니다."""
    # 코드 블록 스타일 적용
    text = re.sub(r'```(.*?)```', apply_code_block_style, text, flags=re.DOTALL)
    # 볼드 스타일 적용
    text = apply_bold_style(text)
    # 맞춤 볼드 스타일 적용
    text = apply_custom_bold_style(text)
    # 맞춤 볼드 스타일 적용 Red
    #text = apply_custom_bold_style_Red(text)
    
    # 함수 스타일 적용
    text = apply_function_style(text)
    
    # 들여쓰기 스타일 적용
    text = apply_indent_style(text)
    
    # HTML 줄바꿈 적용
    #text = '<p>' + text.replace('\n', '<br>') + '</p>'

    # HTML 줄바꿈 적용
    text_with_br = text.replace("\n", "<br>")

    # white-space 속성을 적용한 <p> 태그로 텍스트 감싸기
    text = f'<p style="white-space: pre-wrap;">{text_with_br}</p>'

    
    # CSS 스타일 생성
    formatter = HtmlFormatter(style="monokai")
    css_style = formatter.get_style_defs('.highlight')

    # HTML 문서 템플릿
    styled_text = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
    <style type="text/css">
    {css_style}
    body {{
        background-color: {background_color};
        color: {font_color};
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 14px; /* 폰트 크기를 14px로 설정 */
    }}
    </style>
    </head>
    <body>
    {text}
    </body>
    </html>
    """

    return styled_text

# 아래 부분은 메인 로직을 처리합니다.
if __name__ == "__main__":
    # 배경색 및 폰트 색상 지정
    background_color = '#343541'
    font_color = '#FFFFFF'

    # 파일 경로 설정 및 파일 읽기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    response_file_path = os.path.join(script_dir, "..\\output\\10_ResultData.txt")
    try:
        with open(response_file_path, "r", encoding="utf-8") as file:
            example_text = file.read()
    except FileNotFoundError:
        print(f"{response_file_path} 한글 파일을 찾을 수 없습니다.")
        exit()

    # HTML 형식으로 강조된 텍스트 생성 및 파일 저장
    highlighted_text = highlight_text(example_text, background_color, font_color)
    
    # 결과를 파일에 저장
    file_name = "11_highlighted_text.html"
    output_file_path = os.path.join(script_dir, "../output", file_name)

    #output_file_path = os.path.join(script_dir, "10_highlighted_text.html")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(highlighted_text)
    print(f"'{output_file_path}' 한글 파일에 저장되었습니다.")
