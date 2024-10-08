import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QVBoxLayout, QGridLayout, 
QLineEdit, QSizePolicy, QPushButton, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl, Qt


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 클래스 내에서 사용할 변수들
        self.keyword = ''
        self.currentDir = ''
        self.currentDB = None
        
        # 레이아웃 설정
        mainLayout = QVBoxLayout()
        horizontalLayout = QGridLayout()
        gridLayout = QGridLayout()
        gridLayout.addLayout(horizontalLayout, 0, 0)
        mainLayout.addLayout(gridLayout)
        
        # 검색어 입력창
        self.keywordLine = self.createLine('키워드 입력')
        self.keywordLine.returnPressed.connect(self.updateResultBox)
        horizontalLayout.addWidget(self.keywordLine, 0, 0)

        # 검색 버튼
        searchBtn = self.createButton('검색')
        searchBtn.clicked.connect(self.updateResultBox)
        horizontalLayout.addWidget(searchBtn, 0, 3, 1, 3)
        
        # 테이블(검색 결과창)
        resultBox = self.createResultTable()
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
        # 해상도에 맞게 화면 설정
        screen = QApplication.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height()
        window_width = int(width * 0.9)
        window_height = int(height * 0.6)
        self.resize(window_width, window_height)

        # 아이콘 설정 / 상대경로
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'Icon2.png')
        self.setWindowIcon(QIcon(icon_path))
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
            border-color: gray;
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
            border-color: gray;
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
    def createResultTable(self):
        columns = ['이름', '확장자', '경로', '키워드']
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.cellClicked.connect(self.linkToLocalFile)

        return self.tableWidget

    #################################
    ##### 버튼 시그널 위한 메소드 #####
    #################################

    def linkToLocalFile(self, row, column):
        if column == 2:
            item = self.tableWidget.item(row, column)
            if item:
                url = item.data(Qt.DisplayRole)
                QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    def updateResultBox(self):
        # 키워드 업데이트
        self.keyword = self.keywordLine.text()

        # 테이블 초기화/업데이트
        self.tableWidget.setRowCount(0)

        # 결과 받아 오기
        # Capstone_Backend.explore_the_path(self.currentDir, self.currentDB)
        # 횡 스크롤 설정
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 픽셀 단위 스크롤
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 스크롤바 항상 켜짐
        resultList = self.currentDB.getFileInfoFromDB(self.keyword)
        ### row 업데이트 ###
        for i in range(0, len(resultList)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(resultList[i][1])) # 이름
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(resultList[i][2])) # 확장자
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(resultList[i][0] + '/' + resultList[i][1] + '.' + resultList[i][2])) # 경로
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(resultList[i][3])) # 태그

    def setCurrentDir(self, dir):
        self.currentDir = dir

    def setDB(self, db):
        self.currentDB = db

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = SearchWindow()
    mainWindow.show()
    app.exec_()