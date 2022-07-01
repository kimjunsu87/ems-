# EMS 대쉬보드 앱

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import json
import paho.mqtt.client as mqtt 
import time
import datetime as dt

import dashboard_rc  # 리소스파일 추가

# pip install PyMySQL
import pymysql

# pip install pyqtgraph
# pip install pyqtchart  
from PyQt5.QtChart import *  #QLineSeries, QChart


broker_url = '127.0.0.1' # 로컬에 mqtt broker같이 설치되어 있으므로

class Worker(QThread):
    sigStatus = pyqtSignal(str) # 연결상테 시그널, 부모클래스 MyApp 전달용
    sigMessage = pyqtSignal(dict) # MQTT Subscribe 시그널, MyApp 전달, 딕셔너리형

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.host = broker_url
        self.port = 1883
        self.client = mqtt.Client(client_id='Dashboard')

    def run(self): # Therad에서는 run() 필수
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/data/')
        self.client.loop_forever()
        

    def onConnect(self, mqttc, obj, flags, rc):
        try:
            print(f'connected with result code > {rc}')
            self.sigStatus.emit('SUCCEED') #MYApp 으로 성공메시지 전달ㄷ
        except Exception as e:
            print(f'error > {e.args}')
            self.sigStatus.emit('FAILED)')


    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}') # 시그널로 전달했으므로 주석처리
        self.sigMessage.emit(json.loads(rcv_msg))

        time.sleep(2.0)

    def mqttloop(self):
        self.client.loop()
        print('MQTT client loop')

class MyApp(QMainWindow):
    isTempAlarmed = False # 알람여부
    isHumidAlarmed = False
    tempData = HumidData = None
    idx = 0
    
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()
        self.initMySQL()  #MySQL 초기화
        self.initThread()
        self.initChart()

    def initChart(self):
        #self.viewLimit = 128  # chart 그릴 갯수 제한
        self.tempData = self.humidData = QLineSeries()
        self.iotChart = QChart()

        # axisX = QDateTimeAxis()
        # axisX.setFormat('HH:mm:ss')
        # axisX.setTickCount(5)
        # dt = QDateTime.currentDateTime()
        # axisX.setRange(dt, dt.addSecs(self.viewLimit))

        # axisY = QValueAxis()
        
    
        # self.iotChart.addAxis(axisX, Qt.AlignBottom)
        # self.iotChart.addAxis(axisY, Qt.Alingnleft)
        # self.tempData.attachAxis(axisX)
        # self.humidData.attachAxis(axisX)
        self.iotChart.addSeries(self.tempData)
        self.iotChart.addSeries(self.humidData)
        self.iotChart.layout().setContentsMargins(5, 5, 5, 5)
        
        self.dataView.setChart(self.iotChart)
        self.dataView.setRenderHints(QPainter.Antialiasing)
    #     self.iotData = QLineSeries()
    #     self.iotData.append(0,10)
    #     self.iotData.append(1,20)
    #     self.iotData.append(2,15)
    #     self.iotData.append(3,22)

    #     self.iotChart = QChart()
    #     self.iotChart.addSeries(self.iotData)

    #     self.dataView.setChart(self.iotChart)
        
    def initMySQL(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='bms', password='1234', db='bms', charset='euckr')



    def initThread(self):
        self.myThread = Worker(self)
        self.myThread.sigStatus.connect(self.updateStatus)
        self.myThread.sigMessage.connect(self.updateMessage)
        self.myThread.start()
    
    @pyqtSlot(dict)
    def updateMessage(self, data):
        # 1 딕셔너리 분해
        # 2 Label에 Device명칭 업데이트
        # 3 온도레이블, 습도레이블에 현재 온도 업데이트
        # 4 MySQL DB에 입력
        # 5 이상기온 알람
        # 6 txbLog 로그 출력
        # 7 데이터 차트화
        dev_id = data['DEV_ID']
        self.lblTempTitle.setText(f'{dev_id} Temperature')
        self.lblHumidTitle.setText(f'{dev_id} Temperature')
        temp = data['TEMP']
        humid = data['HUMID']
        self.lblCurrTemp.setText(f'{temp:.1f}')
        self.lblCurrHumid.setText(f'{humid:.0f}')
        # self.txbLog.append(json.dumps(data)) log 사용시 (난 차트 쓰려고 안씀)
        # self.dialTemp.setValue(int(temp)) 다이얼
        # self.dialHumid.setValue(int(humid)) 다이얼  # 다이얼 불필요로 삭제

        #5
        if temp >= 30.0:
            self.lblTempAlarm.setText( f'{dev_id}에서 이상기온 감지')
            # self.btnTempAlarm.Enabled(True) # 버튼활성화
            # self.btnTempStop.setEnabled(False)
            if self.isTempAlarmed == False:
                self.isTempAlarmed = True
                QMessageBox.warning(self, '경고', f'{dev_id}에서 이상기온 감지!!!')
        elif temp <= 28.5:
            self.lblTempAlarm.setText( f'{dev_id} 정상기온')
            self.isTempAlarmed = False
            # self.btnTempAlarm.setEnabled(False) # 버튼 비활성화
            # self.btnTempStop.setEnabled(True)

        # if humid >= 99.0:
        #     self.lblHumidAlarm.setText(f'{dev_id} 이상습도감지')
        #     if self.isHumidAlarmed == False:
        #         self.isHumidAlarmed = True
        #         QMessageBox.warning(self, 'rudrh', f'{dev_id}에서 이상습도 감지!!!')
        # elif humid <= 90.0:
        #     self.lblHumidAlarm

        # 4 DB입력
        self.conn = pymysql.connect(host='127.0.0.1', user='bms', password='1234', db='bms', charset='euckr')
        curr_dt = data['CURR_DT']
        query = '''INSERT INTO ems_data
                        (dev_id, curr_dt, temp, humid)
                    VALUES
                        (%s, %s, %s, %s)'''

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (dev_id, curr_dt, temp, humid))
                self.conn.commit()
                print('DB Inserted!')
        # 7
        self.updateChart(curr_dt, temp, humid)

    def undateChart(self, curr_dt, temp, humid):
        self.tempData.append(self.idx, temp)
        self.humidData.append(self.idx, humid)

        

    @pyqtSlot(str)
    def updateStatus(self, stat):
        print(stat)
        if stat == 'SUCCEED':
            self.lblStatus.setText('Connected')
            self.connFrame.setStyleSheet(
                'background-image: url(:/green);'
                'background-repeat: none;'
                'border: none;'
            )
        else:
            self.lblStatus.setText('Disconnected')
            self.connFrame.setStyleSheet(
                'background-image: url(:/red);'
                'background-repeat: none;'
                'border: none;'
            )
        

    def initUI(self):
        uic.loadUi('./window/ui/dashboard.ui',self)
        self.setWindowIcon(QIcon('iot_64.png'))
        # 화면 정중앙 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        # self.btnTempAlarm.setEnabled(False) # 버튼 비활성화
        # self.btnTempStop.setEnabled(True) 
        self.move(qr.topLeft())
        #위젯 시그널 정의
        self.btnTempAlarm.clicked.connect(self.btnTempAlarmClicked)
        self.btnTempStop.clicked.connect(self.btnTempStopClicked)
        self.btnHumidAlarm.clicked.connect(self.btnHumidAlarmClicked)
        self.btnHumidStop.clicked.connect(self.btnHumidStopClicked)
        self.show()
    
    def btnHumidAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상습도로 제습기 가동')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'DASHBOARD', 'CURR_DT': curr, 'TYPE':'DEHUMD', 'STAT' : 'ON' } #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)
        print('Dehumidufier On Published')
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'ON')

    def btnHumidStopClicked(self):
        QMessageBox.information(self, '정상', '제습기 중지')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'DASHBOARD', 'CURR_DT': curr, 'TYPE':'DEHUMD', 'STAT' : 'OFF' } #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)
        print('Dehumidufier Off Published')
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'OFF')

    def btnTempAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상온도로 에어컨 가동')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'DASHBOARD', 'CURR_DT': curr, 'TYPE':'AIRCON', 'STAT' : 'ON' } #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)
        print('AIRCON On Published')
        self.insertAlarmData('CONTROL', curr, 'AIRCON', 'ON')

    def btnTempStopClicked(self):
        QMessageBox.information(self, '정상', '에어컨 중지')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'DASHBOARD', 'CURR_DT': curr, 'TYPE':'AIRCON', 'STAT' : 'OFF' } #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)
        print('AIRCON Off Published')
        self.insertAlarmData('CONTROL', curr, 'AIRCON', 'OFF')
    
    #이상상태, 정상상태 DB저장 함수
    def insertAlarmData(self, dev_id, curr_dt, types, stat):
        self.conn = pymysql.connect(host='127.0.0.1', user='bms', password='1234', db='bms', charset='euckr')
        query = '''INSERT INTO ems_alarm
                        (dev_id, curr_dt, type, stat)
                    VALUES
                        (%s, %s, %s, %s)'''

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (dev_id, curr_dt, types, stat))
                self.conn.commit()
                print('Alarm Inserted!')

    # 종료 시그널
    def closeEvent(self, signal):
        ans = QMessageBox.question(self, '종료', '종료하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.conn.close() # DB 접속 끊기
            signal.accept()
        else:
            signal.ignore()

    def showTime(self):
        today = QDateTime.currentDateTime()
        currDate = today.date()
        currTime = today.time()
        currDay = today.toString('dddd')

        self.lblDate.setText(currDate.toString('yyyy-MM-dd'))
        self.lblDay.setText(currDay)
        self.lblTime.setText(currTime.toString('HH:mm'))
        if today.time().hour() > 5 and today.time().hour() < 12:
            self.lblGreeting.setText('Good Morning!')
        elif today.time().hour() >= 12 and today.time().hour() < 18:
            self.lblGreeting.setText('Good Afternoon!')
        elif today.time().hour() >= 18:
            self.lblGreeting.setText('Good Evening!')

    def showWeather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather?q=seoul&appid=0a9f6aeb854114111d15d53b5a76469d&lang=kr&units=metric'
        result = requests.get(url)
        result = json.loads(result.text)
        weather = result['weather'][0]['main'].lower()
        self.weatherFrame.setStyleSheet(
            (
                f'background-image: url(:/{weather});'
                'background-repeat: none;'
                'border: none;'
            )
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()