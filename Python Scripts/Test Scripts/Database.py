import sqlite3 
import os


class DB():
    sql=""
    # folderPath = r'/Users/hj/Library/Mobile Documents/com~apple~CloudDocs/24-1학기/인공지능/'                 # 탐색을 원하는 원하는 폴더 경로

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cur = self.conn.cursor()	# 커서생성

        sql = "CREATE TABLE IF NOT EXISTS fileTable (path varchar(1000), name varchar(255) , extensionName char(15), tags varchar(255) )"	# 실행할 sql문
        self.cur.execute(sql)	# 커서로 sql문 실행 여기까지     

    def getFileInfo (self, folder_path) :
        #file_sizes = []
        file_names = []
        file_extensions = []

        file_list = os.listdir(folder_path)  
        for file in file_list:
            file_names.append(os.path.splittext(file)[0])
            file_extensions.append(os.path.splittext(file)[1])
            #file_sizes.append(str((os.path.getsize(folder_path + '/' + file))))

        return file_names, file_extensions

    # db에 파일 정보 및 태그 저장
    def insertFileInfo(self, root, name, tag) :
        filename = name.split('.')[0]
        fileextension = name.split('.')[1]
        
        tags = tag[0]
        for i in tag :
            if i == tag[0] : pass
            else : tags += ", " + i
        sql = "INSERT INTO fileTable VALUES('" + root + "','" + filename + "','" + fileextension + "','" + tags + "')"	# sql변수에 INSERT SQL문 입력
        self.cur.execute(sql)	# 커서로sql 실행

    def getFileInfoFromDB(self, keyword):
        likeKeyword = '%{0}%'.format(keyword)
        query = 'SELECT * FROM filetable WHERE tags LIKE ?' # ?는 플레이스 홀더로 likeKeyword로 대체
        return list(self.cur.execute(query, (likeKeyword,)))
        

if __name__ == "__main__":
    # 메인 코드
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()	# 커서생성

    sql = "CREATE TABLE IF NOT EXISTS fileTable (path varchar(1000), name varchar(255) , extensionName char(15), tags varchar(255) )"	# 실행할 sql문
    cur.execute(sql)	# 커서로 sql문 실행 여기까지

    # 데이터베이스 확인 코드
    cur.execute('SELECT * FROM filetable')
    for row in cur:
        print(row)
        
    conn.commit()	# 저장
    conn.close()	# 종료
