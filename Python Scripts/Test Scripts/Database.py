import sqlite3 
import os


class DB():
    sql=""
    # folderPath = r'/Users/hj/Library/Mobile Documents/com~apple~CloudDocs/24-1학기/인공지능/'                 # 탐색을 원하는 원하는 폴더 경로

    def __init__(self):
        self.conn = sqlite3.connect('./filedata.db')
        self.cur = self.conn.cursor()	# 커서생성

        sql = "CREATE TABLE IF NOT EXISTS fileTable (path varchar(1000), name varchar(255) , extensionName char(15), tags varchar(255) )"	# 실행할 sql문
        self.cur.execute(sql)	# 커서로 sql문 실행 여기까지

    # db에 파일 정보 및 태그 저장
    def insertFileInfo(self, root, name, tag) :
        # filename = name.split('.')[0]
        fileextension = name.split('.')[-1]
        filename = name[0:len(name) - len(fileextension) - 1]
        
        tags = tag[0]
        for i in tag :
            if i == tag[0] : pass
            else : tags += ", " + i
        sql = "INSERT INTO fileTable VALUES('" + root + "','" + filename + "','" + fileextension + "','" + tags + "')"	# sql변수에 INSERT SQL문 입력
        self.cur.execute(sql)	# 커서로sql 실행

    def getFileInfoFromDB(self, keyword):
        likeKeyword = '%{0}%'.format(keyword)
        query = 'SELECT * FROM fileTable WHERE tags LIKE ?' # ?는 플레이스 홀더로 likeKeyword로 대체
        temp = list(self.cur.execute(query, (likeKeyword,)))
        # self.conn.commit()
        return temp

    # 특정 파일 하나만 삭제하는 메소드
    def deleteFileInfo(self, fileFath, fileName, fileExtensionName) :
        self.cur.execute("DELETE FROM 'fileTable' WHERE path =:PATH AND name =:NAME AND extensionName=:EXTENSIONNAME",{"PATH":fileFath, "NAME":fileName, "EXTENSIONNAME":fileExtensionName})
        print(fileFath, fileName, "삭제")
        self.conn.commit()
        
    # 테이블 자체를 모두 삭제하는 메소드
    def deleteTable(self) :
        self.conn.execute("DELETE FROM fileTable").rowcount
        print("모두 삭제")
        self.conn.commit()
        
    # 테이블 내용을 모두 출력하는 메소드
    def pritnTable(self) :
        temp = []
        self.cur.execute('SELECT * FROM fileTable')
        temp = list(self.cur)
        self.conn.commit()
        return temp
            

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
