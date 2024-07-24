import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QVBoxLayout, QGridLayout, 
QLineEdit, QSizePolicy, QPushButton, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QDesktopServices, QScreen
from PyQt5.QtCore import QUrl, Qt

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
<<<<<<< Updated upstream:Python Scripts/Test Scripts/UI/SearchWindow.py
        width = 1600
        height = 720
        self.resize(width, height)
=======
        # 해상도에 맞게 화면 설정
        screen = QApplication.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height()
        window_width = int(width * 0.9)
        window_height = int(height * 0.6)
        self.resize(window_width, window_height)

>>>>>>> Stashed changes:Python Scripts/Test Scripts/UI_SearchWindow.py
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
    def createResultTable(self):
        columns = ['이름', '확장자', '용량', '경로']
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
        if column == 3:
            item = self.tableWidget.item(row, column)
            if item:
                url = item.data(Qt.DisplayRole)
                #url = url.split('"')[1]
                QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    def updateResultBox(self):
        # 키워드 업데이트
        self.keyword = self.keywordLine.text()

        # 테이블 초기화/업데이트
        self.tableWidget.setRowCount(0)

        ### row 업데이트 ###
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        item = QTableWidgetItem('C:/Users/sj/Desktop/SCHOOL/3-2/지구화시대의 역tsdfa.txt')
        self.tableWidget.setItem(rowPosition, 0, item)
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem('txt'))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem('12489172847 Byte'))
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem("C:/Users/sj/Desktop/SCHOOL/3-2/지구화시대의 역사학과 한국사의 재조명/기말.txt"))
        for i in range(1, 30):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem('dasdasdasfsdgds'))


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = SearchWindow()
    mainWindow.show()
    app.exec_()