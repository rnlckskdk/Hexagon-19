import sqlite3 
import os

# 전역변수 선언부
conn = None
cur = None

sql=""
folderPath = r'/Users/hj/Library/Mobile Documents/com~apple~CloudDocs/24-1학기/인공지능/'                 # 탐색을 원하는 원하는 폴더 경로


def getFileInfo (folder_path) :
    file_sizes = []
    file_names = []
    file_extensions = []

    file_list = os.listdir(folder_path)  
    for file in file_list:
        file_names.append(os.path.splitext(file)[0])
        file_extensions.append(os.path.splitext(file)[1])
        file_sizes.append(str((os.path.getsize(folder_path + '/' + file))))

    return file_names, file_extensions, file_sizes



if __name__ == "__main__":
    # 메인 코드
    conn = sqlite3.connect(':memory:') #(host='127.0.0.1', user='root', password='1234', db='pythonDB', charset='utf8mb4')  # 접속정보
    cur = conn.cursor() # 커서생성

    sql = "CREATE TABLE IF NOT EXISTS fileTable (name varchar(255), path varchar(1000), extensionName char(15), volume BIGINT(100) )"   # 실행할 sql문
    cur.execute(sql)    # 커서로 sql문 실행

    file_name, file_extension, file_size = getFileInfo(folderPath)
    
    for i in range(len(file_name)) :
        name = file_name[i]
        extension = file_extension[i]
        size = file_size[i]
        path = folderPath
        sql = "INSERT INTO fileTable VALUES('" + name + "','" + path + "','" + extension + "'," + size + ")"    # sql변수에 INSERT SQL문 입력
        cur.execute(sql)    # 커서로sql 실행

    # 데이터베이스 확인 코  
    cur.execute('SELECT * FROM filetable')
    for row in cur:
        print(row)

        
    conn.commit()   # 저장
    conn.close()    # 종료