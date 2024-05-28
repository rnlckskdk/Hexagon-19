import sys, os
from PyPDF2 import PdfReader # pip install PyPDF2
import docx2txt # pip install docx2txt
import openai
import time
import olefile
from pptx import Presentation
import Database


#입력

"""
처음으로 개발해야 하는 것은 
타겟 폴더를 입력받았을 때
해당 폴더(경로)에서 txt 파일과 pdf 파일을 구분한다

txt 파일 부분에서는 텍스트 추출(읽어내는 것)을 목표로 한다.

얻어내야 하는 것은 제목, 경로, 용량, 확장자 (나중에 추가로 태그까지 저장)

고려해야 할 사항
-> 사용자의 컴퓨터에 라이브러리(모듈)이 설치가 되어있지 않은 경우
-> requiremnet.txt 방법 이용 or 강제로 명령어 실행시켜주는 시스템 콜 이용?


"""

"""
# txt파일 리스트 return
def get_TXT_list(folder_path) :
    txt_list = []
    for alpha in os.listdir(folder_path): # 일일이 list를 전부 확인
        if alpha.endswith("txt"):
            txt_list.append(alpha)
    return txt_list

# pdf파일 리스트 return
def get_PDF_list(folder_path) :
    pdf_list = []
    for alpha in os.listdir(folder_path):
        if alpha.endswith("pdf"):
            pdf_list.append(alpha)
    return pdf_list

# word파일 리스트 return
def get_Word_list(folder_path) :
    word_list = []
    for alpha in os.listdir(folder_path): # 일일이 list를 전부 확인
        if alpha.endswith("docx") and not alpha.startswith("~$"): # doc는 제외
            word_list.append(alpha)
    return word_list


# 리스트 형태로 txt파일 텍스트 추출
def get_Text_from_txt(folder_path) :
    txt_detail = [] # 읽은 내용을 저장할 공간
    txt_list = get_TXT_list(folder_path)
    txt_file_path = [] # 생성했을 때 빈 리스트에서 데이터 접근 => list[i]로 접근 x
    #for txt_file in txt_list:
    #    txt_path.append(os.path.join(folder_path, txt_file))
    # for txt_file_path in txt_path:
    #     with open(txt_file_path, encoding='utf-8') as f:
    #         txt_detail.append(f.read())
    for i in range(len(txt_list)):
        txt_file_path.append(os.path.join(folder_path, txt_list[i]))
        f = open(txt_file_path[i], encoding='utf-8')
        RD = f.read() # read
        txt_detail.append(RD) #비어있는 배열에는 [i]쓰는거 아님
    return txt_detail

# 리스트 형태로 pdf파일 텍스트 추출 
def get_Text_from_pdf(folder_path):
    pdf_detail = []
    pdf_list = get_PDF_list(folder_path)
    pdf_file_path = "" # list 사용 x
    for i in range(len(pdf_list)):
        pdf_file_path = os.path.join(folder_path, pdf_list[i]) # 파일의 경로 완성
        RD = PdfReader(pdf_file_path) # PdfReader로 파일 읽어오기
        new_pdf_text = RD.pages 
        page_data = ""
        for i in new_pdf_text:
            one_page = i.extract_text()
            page_data += one_page
        pdf_detail.append(page_data) # pdf 리스트에 맞춰서 텍스트 추출 완료
    return pdf_detail



# word파일 텍스트 추출
# folder_path = "C:\\Users\\최정현\\Desktop"
# file_name = '201911018_최정현.docx'

# def docx_to_txt(folder_path, file_name):
#     # 파일 경로를 올바르게 조합하기
#     file_path = os.path.join(folder_path, file_name)
#     # docx2txt를 사용하여 .docx 파일의e 내용을 추출 (전체 텍스트를 하나의 문자열로 반환)
#     text = docx2txt.process(file_path)
    
#     return [text]  # 전체 텍스트를 하나의 리스트 인덱스에 담아 반환

# extracted_text = docx_to_txt(folder_path, file_name)
# print("추출된 텍스트:", extracted_text)

# def get_Text_from_word(folder_path):
#     # 파일 경로를 올바르게 조합하기
#     word_detail = []
#     word_list = get_Word_list(folder_path)
#     word_file_path = ""
#     for i in range(len(word_list)):
#         word_file_path = os.path.join(folder_path, word_list[i])
#         # docx2txt를 사용하여 .docx 파일의 내용을 추출 (전체 텍스트를 하나의 문자열로 반환)
#         text = docx2txt.process(word_file_path)
#         word_detail.append(text)
#     return word_detail # 전체 텍스트를 하나의 리스트 인덱스에 담아 반환
"""
def get_Word_list(folder_path):    
    return [f for f in os.listdir(folder_path) if f.endswith('.docx') and not f.startswith('~$')]
""" 


def get_Text_from_word(folder_path):
    # error = 0
    word_detail = []
    word_list = get_Word_list(folder_path)
    for word_file in word_list:
        word_file_path = os.path.join(folder_path, word_file)
        # try:
            # docx2txt를 사용하여 .docx 파일의 내용을 추출
        text = docx2txt.process(word_file_path)
        word_detail.append(text)
        # except Exception as e:
        #     error += 1
        #     # 예외 발생 시, 해당 파일에 대한 오류 정보를 건너 뜀
    return word_detail








# 파일 정보 return
def getFileInfo(folder_path) :
    file_sizes = []
    file_names = []
    file_extensions = []

    file_list = os.listdir(folder_path)  
    for file in file_list:
        file_names.append(os.path.splitext(file)[0])
        file_extensions.append(os.path.splitext(file)[1])
        file_sizes.append(str((os.path.getsize(folder_path + '/' + file))))

    return file_names, file_extensions, file_sizes

"""

# open ai api 이용

# 여기에 키 들어감

def openaiAPI(data): 
    response = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": "You are a sophisticated keyword extraction system."},
            {"role": "user", "content": "Please Extract 10 relevant keywords from the following text, numbered one by one."},
            {"role": "user", "content": data }
        ],
        temperature=0, # 예측 가능성, 무작위성 , 낮을수록 결정록적이고 일관된 텍스트 
        top_p=0,      # 다양성 , 상위
    )
    return response


# 모든 하위폴더를 탐색하는 코드
# 사용 결과 => dirpath, dirnames, filenames
# 파일의 위치를 정확히 알아야 하는가? yes
# 무엇이 필요한가? 
# 확장자명, 
# completions 리스트 사용
def explore_the_path(folder_path, db):
    print("in path")
    ai_result = ""
    temp_paths = []
    for (root, dirs, files) in os.walk(folder_path):
        for file in files:
            temp_paths.append(os.path.join(root, file))
            if os.path.getsize(os.path.join(root,file)) < 4 * 1024 * 1024:  # 파일 크기가 4MB 이하인지 확인
                if file.endswith('txt'):
                    f = open(os.path.join(root,file), encoding='utf-8')
                    RD = f.read() # read
                    # txt에서 text 추출 완료
                    ai_result = openaiAPI(RD)
                    keywords_text = ai_result.choices[0].message.content
                    keywords_list = [line.split(". ", 1)[1].strip() for line in keywords_text.strip().split("\n") if ". " in line]
                    db.insertFileInfo(root, file, keywords_list)
                    # print("파일경로 : ",root, "\n","파일이름 : ",file, "\n", ai_result.choices[0].message.content, sep="", end="\n\n")

                elif file.endswith('pdf'):
                    RD = PdfReader(os.path.join(root,file)) # PdfReader로 파일 읽어오기
                    new_pdf_text = RD.pages 
                    page_data = ""
                    for i in new_pdf_text:
                        one_page = i.extract_text()
                        page_data += one_page
                    # pdf에서 text 추출 완료
                    ai_result = openaiAPI(page_data)
                    keywords_text = ai_result.choices[0].message.content
                    keywords_list = [line.split(". ", 1)[1].strip() for line in keywords_text.strip().split("\n") if ". " in line]
                    db.insertFileInfo(root, file, keywords_list)
                    # print("파일경로 : ",root, "\n","파일이름 : ",file, "\n", ai_result.choices[0].message.content, sep="", end="\n\n")

                elif file.endswith('docx') and not file.startswith('~$'):
                    text = docx2txt.process(os.path.join(root,file))
                    # word에서 text 추출 완료
                    ai_result = openaiAPI(text)
                    keywords_text = ai_result.choices[0].message.content
                    keywords_list = [line.split(". ", 1)[1].strip() for line in keywords_text.strip().split("\n") if ". " in line]
                    db.insertFileInfo(root, file, keywords_list)
                    # print("파일경로 : ",root, "\n","파일이름 : ",file, "\n", ai_result.choices[0].message.content, sep="", end="\n\n")

                elif file.endswith('hwp'):
                    RD = olefile.OleFileIO(os.path.join(root,file))
                    encoded_text = RD.openstream('PrvText').read()
                    decoded_text = encoded_text.decode('utf-16')
                    ai_result = openaiAPI(decoded_text)
                    keywords_text = ai_result.choices[0].message.content
                    keywords_list = [line.split(". ", 1)[1].strip() for line in keywords_text.strip().split("\n") if ". " in line]
                    db.insertFileInfo(root, file, keywords_list)
                    # print("파일경로 : ",root, "\n","파일이름 : ",file, "\n", ai_result.choices[0].message.content, sep="", end="\n\n")

                elif file.endswith('pptx'):
                    RD = Presentation(os.path.join(root,file))
                    text_runs = []
                    for slide in RD.slides:
                        for shape in slide.shapes:
                            if not shape.has_text_frame:
                                continue
                            for paragraph in shape.text_frame.paragraphs:
                                for run in paragraph.runs:
                                    text_runs.append(run.text)
                    combined_text = "\n".join(text_runs)
                    ai_result = openaiAPI(combined_text)
                    keywords_text = ai_result.choices[0].message.content
                    keywords_list = [line.split(". ", 1)[1].strip() for line in keywords_text.strip().split("\n") if ". " in line]
                    db.insertFileInfo(root, file, keywords_list)
                    # print(keywords_text)
                    # print("폴더경로 : ",root, "\n","파일이름 : ",file, "\n", ai_result.choices[0].message.content, sep="", end="\n\n")
    
    print("out path")

"""
# db에 정보를 보내기


folder_path = 'C:\\Users\\최정현\\Desktop\\파일_읽기_ChatGPT'

explore_the_path(folder_path)
"""
if __name__ == "__main__":
    explore_the_path("C:/Users/sj/Desktop/임시", None)