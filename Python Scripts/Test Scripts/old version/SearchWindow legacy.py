import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QVBoxLayout, QGridLayout, 
QLineEdit, QSizePolicy, QPushButton, QTextBrowser)
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 클래스 내에서 사용할 변수들
        self.keyword = ''
        
        # 레이아웃 설정
        mainLayout = QVBoxLayout()
        horizontalLayout = QGridLayout()
        gridLayout = QGridLayout()
        gridLayout.addLayout(horizontalLayout, 0, 0)
        mainLayout.addLayout(gridLayout)
        
        # 검색어 입력창
        self.keywordLine = self.createLine('키워드 입력')
        horizontalLayout.addWidget(self.keywordLine, 0, 0)

        # 검색 버튼, 결과창 업데이트 기능도 함계 있어야 될듯함
        searchBtn = self.createButton('검색')
        # searchBtn.clicked.connect()
        horizontalLayout.addWidget(searchBtn, 0, 3, 1, 3)
        
        # 텍스트 브라우저(검색 결과창)
        resultBox = self.createResultBox()
        gridLayout.addWidget(resultBox, 1, 0)

        # ui 설정
        self.setLayout(mainLayout)
        self.setupUI()


    ###########################
    ##### 셋업/생성 메소드 #####
    ###########################

    # 윈도우 생성 시 화면 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 윈도우 기본 설정
    def setupUI(self):
        title = '검색'
        self.setWindowTitle(title)
        width = 1600
        height = 720
        self.resize(width, height)
        self.setWindowIcon(QIcon('Icon2.png'))
        self.center()

    # 버튼 생성 메소드
    def createButton(self, text):
        btnStyle = '''
        QPushButton
        {
            background-color: white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: black;
            font: bold 23px;
            min-width: 10em;
            padding: 6px;
        }
        QPushButton:pressed
        {
            background-color: gray;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: black;
            font: bold 23px;
            min-width: 10em;
            padding: 6px;
        }
        '''
        btn = QPushButton(text)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setStyleSheet(btnStyle)
        return btn

    # 라인 생성 메소드
    def createLine(self, text):
        lineStyle = '''
        QLineEdit
        {
            font: bold
        }
        '''
        dirLine = QLineEdit(self)
        dirLine.setPlaceholderText(text)
        dirLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        dirLine.setStyleSheet(lineStyle)
        return dirLine

    # 결과 창 생성 메소드
    def createResultBox(self):
        # 파일 접근위한 함수
        def handle_links(url):
            if not url.scheme():
                url = QUrl.fromLocalFile(url.toString())
            QDesktopServices.openUrl(url)
            
        ################################ 변경 필요 #######################################
        resultTextFormat = '''
        <p>파일 이름 &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; 
        확장자 &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; 
        용량 &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
        파일 경로</p>
        '''
        # 경로는 back slash가 안됨 forward slash로 구성되야함 # 현재 유니코드로 인코딩된 문자 인식 못함
        resultItemPath = "C:/Users/sj/Desktop/SCHOOL/3-2/지구화시대의 역사학과 한국사의 재조명/기말.txt"

        resultItemFormat = '''
        <br><a href="{0}">{1}</a></br>
        '''.format(resultItemPath, resultItemPath)

        resultItemPath1 = "C:/Users/sj/Desktop/dasdasd/dasda/dfsfsd.txt"

        resultItemFormat1 = '''
        <br><a href="{0}">{1}</a></br>
        '''.format(resultItemPath1, resultItemPath1)
        # 결과 포맷 추가 구현 필요
        ################################ 변경 필요 #######################################

        resultBox = QTextBrowser()
        resultBox.setAcceptRichText(True)
        resultBox.setOpenExternalLinks(True)
        resultBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # 출력
        resultBox.anchorClicked.connect(handle_links)
        resultBox.append(resultTextFormat)
        # 출력 포맷도 조정(업데이트 함수 추가하여 검색 시 업데이트 되게끔)
        resultBox.insertHtml(resultItemFormat)
        resultBox.insertHtml(resultItemFormat1)
        return resultBox


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = SearchWindow()
    mainWindow.show()
    app.exec_()