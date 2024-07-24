from openai import OpenAI
from PyPDF2 import PdfReader
import os

# chat gpt api key 입력, 각자 본인 api key 사용
# 목표 폴더 경로, pdf와 텍스트 파일이 있는 임의의 폴더로 변경
dir_path = "C:/Users/sj/Desktop/dfg"
# 폴더 내 파일들 경로 저장 리스트
file_paths = []
# chatGPT와 통신 후 반환된 completion 객체 저장 리스트
completions = []

# 경로 읽기
def PathRead():
    temp_paths = []
    for (root, dirs, files) in os.walk(dir_path):
        for file in files:
            temp_paths.append(os.path.join(root, file))
    return temp_paths

# 서버와 통신
def CommunicateGPT(data):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "다음 텍스트 블록에서 최대 토큰 수 만큼 키워드를 추출, 각 키워드를 번호 순으로 표기"},
            {"role": "user", "content": data}
        ],
        temperature=0.5,
        max_tokens=64,
        top_p=1
    )
    return completion

# 뽑아낸 단어 저장
def FileWrite(datas):
    f = open("키워드db.txt", 'w')
    i = 0
    for completion in datas:
        f.write(file_paths[i] + "\n") # 해당 파일의 경로
        i += 1
        f.write(completion.choices[0].message.content) # 그 파일에서 추출한 키워드
        f.write("\n====================\n")
    f.close()


file_paths = PathRead()

# 파일 추출
for path in file_paths:
    if ".txt" in path: # txt 추출
        f = open(path, encoding='utf-8')
        data = f.read()
        completions.append(CommunicateGPT(data))
        f.close()
    elif ".pdf" in path: # pdf 추출(텍스트만), https://wooiljeong.github.io/python/pdf-to-text/
        reader = PdfReader(path)
        pages = reader.pages
        data = ""
        for page in pages:
            sub = page.extract_text()
            data += sub
        completions.append(CommunicateGPT(data))

# 출력
FileWrite(completions)