# 네이버 검색용 UI 실행
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json  # 검색결과를 json 타입으로 받음
import urllib.request  # URL openAPI 검색위해
from urllib.parse import quote
import webbrowser # 웹브라우저 

class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./window/ui/navernews.ui', self)
        self.setWindowIcon(QIcon('naver_icon.png'))

        # 시그널 연결
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)

        self.show()

    def tblResultSelected(self):
        selected = self.tblResult.currentRow()
        url = self.tblReuslt.item(selected, 1).text()
        webbrowser.open(url)


    
    def btnSearchClicked(self):
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
        display_count = 50

        jsonResult = self.getNaverSearch(keyword, search_word, 1, display_count)       # print(jsonResult)


        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))

        self.makeTable(totalResult)

    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result))  # 50
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0,350)
        self.tblResult.setColumnWidth(1,350)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # read only

        # 테이블 위젯설정

        i = 0
        for item in result: # 50번 반복
            title = self.strip_tag(item[0]['title'])
            self.tblResult.setItem(i, 0, QTableWidgetItem(item[0]['title']))
            self.tblResult.setItem(i, 1, QTableWidgetItem(item[0]['org_link']))
            i += 1

    def strip_tag(self, title):
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')  
        ret = ret.replace('&guot;', '')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')   
        return ret          

    def getPostData(self, post):
        temp = []
        title = post['title']
        description = post['description']
        org_link = post['originallink']
        link = post['link']

        temp.append({'title':title, 'description':description, 'org_link':org_link, 'link':link})
        return temp

    # 핵심 함수
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json' \
              f'?query={quote(search)}&start={start}&display={display}'
        req = urllib.request.Request(url)
        # 인증추가
        req.add_header('X-Naver-Client-Id','E0uhRf2oStaKnRgZ0MTz')
        req.add_header('X-Naver-Client-Secret', 'OfbJtRg2Pr')

        res =urllib.request.urlopen(req)  #request 대한 response
        if res.getcode() == 200:
            print('URL requst success')
        else:
            print('URL request failed')

        ret = res.read().decode('utf-8')
        if ret == None:
            return None
        else:
            return json.loads(ret)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()