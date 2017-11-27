#!/usr/bin/python3.5
import sys
import os
from PyQt5.QtGui import  QIcon,QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QMessageBox,QApplication,QMainWindow, QAction, qApp,QFileDialog,QTreeView,QTreeWidgetItem,QLineEdit,QLabel,QComboBox,QFrame)
from PyQt5.QtWidgets import (QTreeWidgetItemIterator,QTableWidget,QTableWidgetItem)

from PyQt5.QtGui import QFont
from PyQt5 import QtCore

import sqlite3


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

         self.srvList=["",
                               "master_mercury230",
                               "master_modbusRTU",
                               "master_modbusTCP",
                               "master_http",
                               "master_dcon",
                               "master_ping"]
         self.slvList=["","opcUA","modbusTCP"]

         if(os.name=='nt'):

             self.appPath=os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')


             self.imgPath=self.appPath+"img\\"
             self.dbPath=self.appPath+"db\\srvDb.db"

         else:
             self.appPath=os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
             self.imgPath=self.appPath+"img/"
             self.dbPath=self.appPath+"db/srvDb.db"


         self.versionPr='ScadaPy Конфигуратор сервера v.3.11'
         self.setGeometry(400, 200, 1000, 520)
         self.setWindowTitle(self.versionPr)
         self.setWindowIcon(QIcon( self.imgPath+'gnome-monitor.png'))
         self.h=self.frameGeometry().height()

         font = QFont()
         font.setPointSize(12)


         self.label0=QLabel(self)
         self.label0.setFont(font)
         self.label0.move(400, 60)
         self.label0.resize(300,25)
         self.label0.setText("ID сервера")
         self.label00=QLabel(self)
         self.label00.setFont(font)
         self.label00.move(550, 60)
         self.label00.resize(300,25)
         self.label00.setText("")

         self.label1=QLabel(self)
         self.label1.setFont(font)
         self.label1.move(400, 90)
         self.label1.resize(140,25)
         self.label1.setText("Название сервера")
         self.srvName = QLineEdit(self)
         self.srvName.setToolTip('Пример: Сервер Маш.Зала №1')
         self.srvName.move(550, 90)
         self.srvName.setFont(font)
         self.srvName.resize(300,25)

         self.label2=QLabel(self)
         self.label2.setFont(font)
         self.label2.move(400, 120)
         self.label2.resize(140,25)
         self.label2.setText("Slave IP address")
         self.slaveIP = QLineEdit(self)
         self.slaveIP.setToolTip('Пример: 192.168.0.111')
         self.slaveIP.move(550, 120)
         self.slaveIP.setFont(font)
         self.slaveIP.resize(300,25)


         self.label2=QLabel(self)
         self.label2.setFont(font)
         self.label2.move(400, 150)
         self.label2.resize(140,25)
         self.label2.setText("Slave Port")
         self.slavePort = QLineEdit(self)
         self.slavePort.setToolTip('Пример modbus: 502\nПример opcua: 4840')
         self.slavePort.move(550, 150)
         self.slavePort.setFont(font)
         self.slavePort.resize(100,25)

         self.label7=QLabel(self)
         self.label7.setFont(font)
         self.label7.move(680, 150)
         self.label7.resize(140,25)
         self.label7.setText("Timeout")
         self.serverTimeout = QLineEdit(self)
         self.serverTimeout.setToolTip('Пример ms: 1 ')
         self.serverTimeout.move(750, 150)
         self.serverTimeout.setFont(font)
         self.serverTimeout.resize(100,25)




         self.label3=QLabel(self)
         self.label3.setFont(font)
         self.label3.move(400, 180)
         self.label3.resize(140,25)
         self.label3.setText("Тип Master")
         self.label3=QLabel(self)
         self.label3.setFont(font)
         self.label3.move(550, 180)
         self.label3.resize(340,25)
         self.label3.setText("---")

         self.combo1 = QComboBox(self)
         self.combo1.move(550, 210)
         self.combo1.setFont(font)
         self.combo1.resize(320,25)
         self.combo1.addItems(self.srvList)

         self.label4=QLabel(self)
         self.label4.setFont(font)
         self.label4.move(400, 240)
         self.label4.resize(140,25)
         self.label4.setText("Тип Slave")
         self.label4=QLabel(self)
         self.label4.setFont(font)
         self.label4.move(550, 240)
         self.label4.resize(340,25)
         self.label4.setText("---")

         self.combo2 = QComboBox(self)
         self.combo2.move(550, 270)
         self.combo2.setFont(font)
         self.combo2.resize(320,25)
         self.combo2.addItems(self.slvList)

         self.label5=QLabel(self)
         self.label5.setFont(font)
         self.label5.move(400, 300)
         self.label5.resize(140,25)
         self.label5.setText("Порт /dev/tty*")
         self.tty=QLineEdit(self)
         self.tty.setToolTip('Пример linux: /dev/ttyUSB0\nПример windows: com19')
         self.tty.setFont(font)
         self.tty.move(550, 300)
         self.tty.resize(150,25)

         self.label6=QLabel(self)
         self.label6.setFont(font)
         self.label6.move(720, 300)
         self.label6.resize(140,25)
         self.label6.setText("скорость")
         self.ttySpeed=QLineEdit(self)
         self.ttySpeed.setToolTip('Пример : 9600')
         self.ttySpeed.setFont(font)
         self.ttySpeed.move(800, 300)
         self.ttySpeed.resize(150,25)



         exitAction = QAction(QIcon( self.imgPath+'exit.png'), '&Выход', self)
         exitAction.setShortcut('Ctrl+Q')
         exitAction.setStatusTip('Выход из программы')
         exitAction.triggered.connect(qApp.quit)


         addServerAction = QAction(QIcon(self.imgPath+'add.png'), '&Добавить', self)
         addServerAction.setStatusTip('Добавить сервер')
         addServerAction.triggered.connect(self.addNewServer)

         delServerAction = QAction(QIcon(self.imgPath+'button_cancel.png'), '&Удалить', self)
         delServerAction.setStatusTip('Удалить сервер')
         delServerAction.triggered.connect(self.delServer)


         saveServerAction = QAction(QIcon(self.imgPath+'filesave.png'), '&Сохранить', self)
         saveServerAction.setStatusTip('Сохранить сервер')
         saveServerAction.triggered.connect(self.saveServer)

         saveScr = QAction(QIcon(self.imgPath+'bottom.png'), '&Сохранить скрипт', self)
         saveScr.setStatusTip('Сохранить скрипт')
         saveScr.triggered.connect(self.saveScr)

         runScr = QAction(QIcon(self.imgPath+'run.png'), '&Запустить скрипт', self)
         runScr.setStatusTip('Запустить скрипт')
         runScr.triggered.connect(self.runScr)


         menubar = self.menuBar()
         fileMenu = menubar.addMenu('&Команды')
         fileMenu.addAction(addServerAction)
         fileMenu.addAction(delServerAction)
         fileMenu.addAction(saveServerAction)
         fileMenu.addAction(saveScr)
         fileMenu.addAction(runScr)
         fileMenu.addAction(exitAction)


         self.toolbar = self.addToolBar('Выход')
         self.toolbar.addAction(exitAction)
         self.toolbar.addAction(addServerAction)
         self.toolbar.addAction(delServerAction)
         self.toolbar.addAction(saveServerAction)
         self.toolbar.addAction(saveScr)
         self.toolbar.addAction(runScr)




        # self.statusBar().showMessage('Загрузка данных')

         self.treeView = QTreeView(self)
         self.treeView.setFont(font)
         self.treeView.setObjectName("treeView")
         self.model = QStandardItemModel()
         self.treeView.setModel(self.model)
         self.header = ['Название сервера']
         self.model.setHorizontalHeaderLabels(self.header)

         self.sqlLoad()
         self.treeView.clicked.connect(self.onClickItem)





         self.frameTable = QFrame(self)
         self.frameTable.move(380, 350)
         self.frameTable.setFont(font)
         self.frameTable.resize(1350,950)
         self.frameTable.setVisible(True)

         self.addRow = QPushButton(self.frameTable)
         self.addRow.setIcon(QIcon(self.imgPath+'add.png'))
         self.addRow.move(10, 10)
         self.addRow.resize(30,30)
         self.addRow.clicked.connect(self.addRowTable)

         self.saveTable = QPushButton(self.frameTable)
         self.saveTable.setIcon(QIcon(self.imgPath+'filesave.png'))
         self.saveTable.resize(30,30)
         self.saveTable.move(50, 10)
         self.saveTable.clicked.connect(self.saveRowTable)


         self.treeTable = QTableWidget(self.frameTable)
         fontTable = QFont()
         fontTable.setPointSize(10)
         self.treeTable.setFont(fontTable)

         self.show()









    def addRowTable(self):
         self.treeTable.insertRow(self.treeTable.rowCount())


    def getDataPing(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(2)
             self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['IP адрес сервера','Имя переменной'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 380)
             self.treeTable.setColumnWidth(1, 400)



             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select ip,name from  master_ping where serverId = "+self.label00.text())
             dt=cursor.fetchall()
             self.treeTable.setRowCount(len(dt))
             for i in range(0,len(dt)):
                 self.treeTable.setItem(i, 0, QTableWidgetItem(dt[i][0]))
                 self.treeTable.setItem(i, 1, QTableWidgetItem(dt[i][1]))
                 i+=1

    def getDataMercury(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(2)
             self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['Сетевой адрес счетчика','Имя переменной'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 380)
             self.treeTable.setColumnWidth(1, 400)



             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select netAdr, serNum from  master_mercury230 where serverId = "+self.label00.text())
             dt=cursor.fetchall()
             self.treeTable.setRowCount(len(dt))
             for i in range(0,len(dt)):
                 self.treeTable.setItem(i, 0, QTableWidgetItem(dt[i][0]))
                 self.treeTable.setItem(i, 1, QTableWidgetItem(dt[i][1]))
                 i+=1

    def getDataModbusTCP(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(8)
             self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['IP адрес','Порт','Адрес\nRTU','Название регистра','Адрес\nячейки','Кол-во\nячеек','Адрес на\nсервере','Имя переменной'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 110)
             self.treeTable.setColumnWidth(1, 50)
             self.treeTable.setColumnWidth(2, 80)
             self.treeTable.setColumnWidth(3, 220)
             self.treeTable.setColumnWidth(4, 80)
             self.treeTable.setColumnWidth(5, 80)
             self.treeTable.setColumnWidth(6, 80)
             self.treeTable.setColumnWidth(7, 160)



             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select ip,port,adrRtu,reg,fromAdr,fromCount,toAdr,comment serNum from  master_modbusTCP where serverId = "+self.label00.text())
             dt=cursor.fetchall()
             self.treeTable.setRowCount(len(dt))
             for i in range(0,len(dt)):
                 self.treeTable.setItem(i, 0, QTableWidgetItem(dt[i][0]))
                 self.treeTable.setItem(i, 1, QTableWidgetItem(dt[i][1]))
                 self.treeTable.setItem(i, 2, QTableWidgetItem(dt[i][2]))
                 self.treeTable.setItem(i, 3, QTableWidgetItem(dt[i][3]))
                 self.treeTable.setItem(i, 4, QTableWidgetItem(dt[i][4]))
                 self.treeTable.setItem(i, 5, QTableWidgetItem(dt[i][5]))
                 self.treeTable.setItem(i, 6, QTableWidgetItem(dt[i][6]))
                 self.treeTable.setItem(i, 7, QTableWidgetItem(dt[i][7]))
                 i+=1


    def getDataHttp(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(7)
             self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['Адрес http','Название регистра','modbus-Адрес ячейки\nopc-тип переменной','Количество \nячеек','Объект','Login','Password'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 310)
             self.treeTable.setColumnWidth(1, 160)
             self.treeTable.setColumnWidth(2, 150)
             self.treeTable.setColumnWidth(3, 120)
             self.treeTable.setColumnWidth(4, 120)
             self.treeTable.setColumnWidth(5, 120)
             self.treeTable.setColumnWidth(6, 120)


             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select ip,reg,toAdr,fromCount,comment,login,password from  master_http where serverId = "+self.label00.text())
             dt=cursor.fetchall()
             self.treeTable.setRowCount(len(dt))
             for i in range(0,len(dt)):
                 self.treeTable.setItem(i, 0, QTableWidgetItem(dt[i][0]))
                 self.treeTable.setItem(i, 1, QTableWidgetItem(dt[i][1]))
                 self.treeTable.setItem(i, 2, QTableWidgetItem(dt[i][2]))
                 self.treeTable.setItem(i, 3, QTableWidgetItem(dt[i][3]))
                 self.treeTable.setItem(i, 4, QTableWidgetItem(dt[i][4]))
                 self.treeTable.setItem(i, 5, QTableWidgetItem(dt[i][5]))
                 self.treeTable.setItem(i, 6, QTableWidgetItem(dt[i][6]))


                 i+=1




    def getDataDcon(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(4)
             self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['Модель','Адрес\nRTU','Адрес ячейки на\nсервере','Имя переменной'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 110)
             self.treeTable.setColumnWidth(1, 80)
             self.treeTable.setColumnWidth(2, 120)
             self.treeTable.setColumnWidth(3, 320)



             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select model,adrRtu,toAdr,comment from  master_dcon where serverId = "+self.label00.text())
             dt=cursor.fetchall()
             self.treeTable.setRowCount(len(dt))
             for i in range(0,len(dt)):
                 self.treeTable.setItem(i, 0, QTableWidgetItem(dt[i][0]))
                 self.treeTable.setItem(i, 1, QTableWidgetItem(dt[i][1]))
                 self.treeTable.setItem(i, 2, QTableWidgetItem(dt[i][2]))
                 self.treeTable.setItem(i, 3, QTableWidgetItem(dt[i][3]))
                 i+=1

    def getDataModbusRTU(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(6)
             self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['Адрес\nRTU','Название регистра','Адрес\nячейки','Кол-во\nячеек','Адрес на\nсервере','Имя переменной'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 50)
             self.treeTable.setColumnWidth(1, 220)
             self.treeTable.setColumnWidth(2, 80)
             self.treeTable.setColumnWidth(3, 80)
             self.treeTable.setColumnWidth(4, 80)
             self.treeTable.setColumnWidth(5, 220)




             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select adrRtu,reg,fromAdr,fromCount,toAdr,comment serNum from  master_modbusRTU where serverId = "+self.label00.text())
             dt=cursor.fetchall()
             self.treeTable.setRowCount(len(dt))
             for i in range(0,len(dt)):
                 self.treeTable.setItem(i, 0, QTableWidgetItem(dt[i][0]))
                 self.treeTable.setItem(i, 1, QTableWidgetItem(dt[i][1]))
                 self.treeTable.setItem(i, 2, QTableWidgetItem(dt[i][2]))
                 self.treeTable.setItem(i, 3, QTableWidgetItem(dt[i][3]))
                 self.treeTable.setItem(i, 4, QTableWidgetItem(dt[i][4]))
                 self.treeTable.setItem(i, 5, QTableWidgetItem(dt[i][5]))
                 i+=1

    def saveRowTable(self):
             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()


             if(self.label3.text()=="master_ping"):
                 cursor.execute("delete from master_ping where serverId= '"+self.label00.text()+"'" )
                 connDb.commit()

                 for i in range(0,self.treeTable.rowCount()):

                     try:
                         if(     len(self.treeTable.item(i,0).text()) > 0 and
                                 len(self.treeTable.item(i,1).text()) > 0 ):

                             cursor.execute("INSERT INTO master_ping(serverId,ip,name,valid)\
                             VALUES('"+self.label00.text()+"','"+self.treeTable.item(i,0).text()+"'\
                             ,'"+self.treeTable.item(i,1).text()+"',1)" )
                             connDb.commit()
                     except Exception as e:
                     #print(e)
                         pass
                     i+=1
                 self.getDataPing()





             if(self.label3.text()=="master_mercury230"):
                 cursor.execute("delete from master_mercury230 where serverId= '"+self.label00.text()+"'" )
                 connDb.commit()

                 for i in range(0,self.treeTable.rowCount()):
                     try:
                         if(     len(self.treeTable.item(i,0).text()) > 0 and
                                 len(self.treeTable.item(i,1).text()) > 0 ):

                             cursor.execute("INSERT INTO master_mercury230(serverId,netAdr,serNum,valid)\
                             VALUES('"+self.label00.text()+"','"+self.treeTable.item(i,0).text()+"'\
                             ,'"+self.treeTable.item(i,1).text()+"',1)" )
                             connDb.commit()
                     except Exception as e:
                     #print(e)
                         pass
                     i+=1
                 self.getDataMercury()


             if(self.label3.text()=="master_modbusTCP"):
                 cursor.execute("delete from master_modbusTCP where serverId= '"+self.label00.text()+"'" )
                 connDb.commit()

                 for i in range(0,self.treeTable.rowCount()):
                         try:
                             if(     len(self.treeTable.item(i,0).text()) > 0 and
                                     len(self.treeTable.item(i,1).text()) > 0 and
                                     len(self.treeTable.item(i,2).text()) > 0 and
                                     len(self.treeTable.item(i,3).text()) > 0 and
                                     len(self.treeTable.item(i,4).text()) > 0 and
                                     len(self.treeTable.item(i,5).text()) > 0 and
                                     len(self.treeTable.item(i,6).text()) > 0 and
                                     len(self.treeTable.item(i,7).text()) > 0 ):

                                 cursor.execute("INSERT INTO master_modbusTCP(serverId,ip,port,adrRtu,reg,fromAdr,fromCount,toAdr,comment,valid)\
                                 VALUES('"+self.label00.text()+"',\
                                 '"+self.treeTable.item(i,0).text()+"',\
                                 '"+self.treeTable.item(i,1).text()+"',\
                                 '"+self.treeTable.item(i,2).text()+"',\
                                 '"+self.treeTable.item(i,3).text()+"',\
                                 '"+self.treeTable.item(i,4).text()+"',\
                                 '"+self.treeTable.item(i,5).text()+"',\
                                 '"+self.treeTable.item(i,6).text()+"',\
                                 '"+self.treeTable.item(i,7).text()+"',\
                                 1)" )
                                 connDb.commit()
                         except Exception as e:
                             #print(e)
                             pass
                         i+=1
                 self.getDataModbusTCP()

             if(self.label3.text()=="master_modbusRTU"):
                 cursor.execute("delete from master_modbusRTU where serverId= '"+self.label00.text()+"'" )
                 connDb.commit()

                 for i in range(0,self.treeTable.rowCount()):
                         try:
                             if(     len(self.treeTable.item(i,0).text()) > 0 and
                                     len(self.treeTable.item(i,1).text()) > 0 and
                                     len(self.treeTable.item(i,2).text()) > 0 and
                                     len(self.treeTable.item(i,3).text()) > 0 and
                                     len(self.treeTable.item(i,4).text()) > 0 and
                                     len(self.treeTable.item(i,5).text()) > 0 ):

                                 cursor.execute("INSERT INTO master_modbusRTU(serverId,adrRtu,reg,fromAdr,fromCount,toAdr,comment,valid)\
                                 VALUES('"+self.label00.text()+"',\
                                 '"+self.treeTable.item(i,0).text()+"',\
                                 '"+self.treeTable.item(i,1).text()+"',\
                                 '"+self.treeTable.item(i,2).text()+"',\
                                 '"+self.treeTable.item(i,3).text()+"',\
                                 '"+self.treeTable.item(i,4).text()+"',\
                                 '"+self.treeTable.item(i,5).text()+"',\
                                 1)" )
                                 connDb.commit()
                         except Exception as e:
                             #print(e)
                             pass
                         i+=1
                 self.getDataModbusRTU()


             if(self.label3.text()=="master_dcon"):
                 cursor.execute("delete from master_dcon where serverId= '"+self.label00.text()+"'" )
                 connDb.commit()

                 for i in range(0,self.treeTable.rowCount()):
                         try:
                             if(     len(self.treeTable.item(i,0).text()) > 0 and
                                     len(self.treeTable.item(i,1).text()) > 0 and
                                     len(self.treeTable.item(i,2).text()) > 0 and
                                     len(self.treeTable.item(i,3).text()) > 0  ):

                                 cursor.execute("INSERT INTO master_dcon (serverId,model,adrRtu,toAdr,comment,valid)\
                                 VALUES('"+self.label00.text()+"',\
                                 '"+self.treeTable.item(i,0).text()+"',\
                                 '"+self.treeTable.item(i,1).text()+"',\
                                 '"+self.treeTable.item(i,2).text()+"',\
                                 '"+self.treeTable.item(i,3).text()+"',\
                                 1)" )
                                 connDb.commit()
                         except Exception as e:
                             #print(e)
                             pass
                         i+=1
                 self.getDataDcon()

             if(self.label3.text()=="master_http"):
                 cursor.execute("delete from master_http where serverId= '"+self.label00.text()+"'" )
                 connDb.commit()

                 for i in range(0,self.treeTable.rowCount()):
                         try:
                             if(     len(self.treeTable.item(i,0).text()) > 0 and
                                     len(self.treeTable.item(i,1).text()) > 0 and
                                     len(self.treeTable.item(i,2).text()) > 0 and
                                     len(self.treeTable.item(i,3).text()) > 0  ):

                                 cursor.execute("INSERT INTO master_http (serverId,ip,reg,toAdr,fromCount,comment,login,password,valid)\
                                 VALUES('"+self.label00.text()+"',\
                                 '"+self.treeTable.item(i,0).text()+"',\
                                 '"+self.treeTable.item(i,1).text()+"',\
                                 '"+self.treeTable.item(i,2).text()+"',\
                                 '"+self.treeTable.item(i,3).text()+"',\
                                 '"+self.treeTable.item(i,4).text()+"',\
                                 '"+self.treeTable.item(i,5).text()+"',\
                                 '"+self.treeTable.item(i,6).text()+"',\
                                 1)" )
                                 connDb.commit()
                         except Exception as e:
                             print(e)
                             pass
                         i+=1
                 self.getDataHttp()







    def truePanel (self,index):
         if(index == 'master_ping'):
             self.getDataPing()

         if(index == 'master_mercury230'):
             self.getDataMercury()
         if(index == 'master_modbusTCP'):
             self.getDataModbusTCP()
         if(index == 'master_modbusRTU'):
             self.getDataModbusRTU()
         if(index == 'master_dcon'):
             self.getDataDcon()
         if(index == 'master_http'):
             self.getDataHttp()



    def onClickItem (self):
         self.treeTable.clear()
         self.treeTable.setRowCount(0)
         self.srvName.setText("")
         self.label00.setText("")
         self.slaveIP.setText("")
         self.slavePort.setText("")
         self.label3.setText("")
         self.tty.setText("")
         self.ttySpeed.setText("")
         self.label4.setText("")
         self.serverTimeout.setText("")



         try:

             self.slaveIP.setEnabled(True)
             self.slavePort.setEnabled(True)
             self.tty.setEnabled(True)
             self.ttySpeed.setEnabled(True)

             index_list =[i.data() for i in self.treeView.selectedIndexes()]
             s=index_list[0].split(':')
             self.srvName.setText(s[1])
             self.label00.setText(s[0])

             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select ip, port,stype,mtype,tty,speed,timeout from  servers where id = "+s[0])
             dt=cursor.fetchone()
             self.slaveIP.setText(dt[0])
             self.slavePort.setText(dt[1])
             self.label4.setText(dt[2])
             self.label3.setText(dt[3])
             self.tty.setText(dt[4])
             self.ttySpeed.setText(dt[5])
             self.serverTimeout.setText(dt[6])

             self.slvList[0]=dt[2]
             self.srvList[0]=dt[3]
             self.truePanel (self.label3.text())



         except Exception as e:
             index_list =[i.data() for i in self.treeView.selectedIndexes()]
             self.srvName.setText(index_list[0])
             self.slaveIP.setEnabled(False)
             self.slavePort.setEnabled(False)
             self.tty.setEnabled(False)
             self.ttySpeed.setEnabled(False)
            # print(e)

         self.combo1.clear()
         self.combo1.addItems(self.srvList)
         self.combo2.clear()
         self.combo2.addItems(self.slvList)



    def addNewServer(self):
         sender = self.sender()
         self.statusBar().showMessage('Добавление нового сервера')
         self.model.appendRow(QStandardItem("Новый Сервер "))






    def closeEvent(self, event):
         reply = QMessageBox.question(self, 'Сообщение', "Вы уверены, что хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
         if reply == QMessageBox.Yes:
            event.accept()
         else:
             event.ignore()

    def resizeEvent(self,event):
         self.h=self.frameGeometry().height()
         self.treeView.setGeometry(QtCore.QRect(0, 60, 350, self.h-120))
         self.treeTable.setGeometry(QtCore.QRect(10, 50, 1140, self.h-460))
         self.frameTable.setGeometry(QtCore.QRect(380, 350, 1150, self.h-400))



    def sqlLoad(self):
         connDb = sqlite3.connect(self.dbPath)
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT name, id FROM servers where valid=1 ORDER BY id'):
             self.model.appendRow(QStandardItem(str(row[1])+":"+row[0]))

    def saveServer(self):
         self.treeTable.clear()
         self.truePanel ("")
         connDb = sqlite3.connect(self.dbPath)
         cursor = connDb.cursor()
         if(len(self.label00.text())>0 and int(self.label00.text()) >0):
             if(len(self.srvName.text()) > 1):
                 connDb.execute("update servers set name ='"+self.srvName.text()+ "', ip = '"+self.slaveIP.text()+"', port = '"+self.slavePort.text()+"'\
                 ,mtype='"+self.combo1.currentText()+"',stype='"+self.combo2.currentText()+"',tty='"+self.tty.text()+"'\
                 ,speed='"+self.ttySpeed.text()+"',timeout='"+self.serverTimeout.text()+"' where id = "+self.label00.text()+" ")
                 connDb.commit()
                 cursor.execute("select ip, port, mtype,stype,tty,speed,timeout from  servers where id = "+self.label00.text())
                 dt=cursor.fetchone()
                 self.slaveIP.setText(dt[0])
                 self.slavePort.setText(dt[1])
                 self.label3.setText(dt[2])
                 self.label4.setText(dt[3])
                 self.tty.setText(dt[4])
                 self.ttySpeed.setText(dt[5])
                 self.slvList[0]=dt[3]
                 self.srvList[0]=dt[2]
                 self.serverTimeout.setText(dt[6])

         else:
             try:
                 if(len(self.srvName.text()) > 1):
                     cursor.execute("INSERT INTO servers(name,valid)  VALUES( '"+self.srvName.text()+"',1)" )



                     connDb.commit()
             except Exception as e:
                 print(e)
                 pass

         self.model.clear()
         self.model.setHorizontalHeaderLabels(self.header)
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT name, id FROM servers where valid=1 ORDER BY id'):
             self.model.appendRow(QStandardItem(str(row[1])+":"+row[0]))
         self.combo1.clear()
         self.combo1.addItems(self.srvList)
         self.combo2.clear()
         self.combo2.addItems(self.slvList)
         self.truePanel (self.label3.text())

    def saveScr(self):
             pathFolder = self.appPath
             if(os.name=='nt'):
                 slash='\\'
                 bat='.bat'
                 rem ='rem '
                 command = 'start '
             else:
                 slash='/'
                 bat='.sh'
                 rem='# '
                 command=''

             f=open(pathFolder +'scr'+slash+'start_'+self.label00.text() + bat,'w')
             f.write(rem+'Скрипт создан в программе \''+self.versionPr+'\'\n')
             f.write(rem+'Название сервера \''+self.srvName.text()+'\'\n')
             f.write(rem+'Slave адрес \''+self.slaveIP.text()+'\'\n')
             f.write(rem+'Slave порт \''+self.slavePort.text()+'\'\n')
             f.write(rem+'Тип master \''+self.label3.text()+'\'\n')
             f.write(rem+'Тип slave \''+self.label4.text()+'\'\n')
             f.write(rem+'Интерфейс tty \''+self.tty.text()+'\'\n')
             f.write(rem+'Скорость tty \''+self.ttySpeed.text()+'\'\n')

             if(self.label4.text() == 'opcUA' and self.label3.text() =='master_modbusTCP'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'opcua_master_tcp.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'opcUA' and self.label3.text() =='master_ping'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'opcua_master_ping.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'opcUA' and self.label3.text() =='master_dcon'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'opcua_master_dcon.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'opcUA' and self.label3.text() =='master_mercury230'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'opcua_master_mercury230.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'opcUA' and self.label3.text() =='master_modbusRTU'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'opcua_master_rtu.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'opcUA' and self.label3.text() =='master_http'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'opcua_master_http.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')


             if(self.label4.text() == 'modbusTCP' and self.label3.text() =='master_modbusTCP'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'modbustcp_master_tcp.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'modbusTCP' and self.label3.text() =='master_ping'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'modbustcp_master_ping.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'modbusTCP' and self.label3.text() =='master_dcon'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'modbustcp_master_dcon.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'modbusTCP' and self.label3.text() =='master_mercury230'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'modbustcp_master_mercury230.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'modbusTCP' and self.label3.text() =='master_modbusRTU'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'modbustcp_master_rtu.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')
             if(self.label4.text() == 'modbusTCP' and self.label3.text() =='master_http'):
                 f.write(command+sys.executable+' '+pathFolder +'source'+slash+'modbustcp_master_http.py '+self.label00.text() +' '+pathFolder +'db'+slash+'srvDb.db')



             f.close()
             ret = pathFolder +''+slash+'scr'+slash+'start_'+self.label00.text() + bat
             return ret

    def runScr(self):

             if(os.name=='nt'):
                 os.system(self.saveScr())
             else:
                 os.system('chmod 777 '+self.saveScr())
                 os.system('xfce4-terminal --command=\'sudo '+self.saveScr()+'\'')





    def delServer(self):
         self.treeTable.clear()
         self.treeTable.setRowCount(0)
         connDb = sqlite3.connect(self.dbPath)

         if(len(self.label00.text())>0 and int(self.label00.text()) >0):
             if(len(self.srvName.text()) > 1):
                 connDb.execute("update servers set valid=0 where id = "+self.label00.text()+" ")
                 connDb.commit()


         self.model.clear()
         self.model.setHorizontalHeaderLabels(self.header)
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT name, id FROM servers where valid=1 ORDER BY id'):
             self.model.appendRow(QStandardItem(str(row[1])+":"+row[0]))

         self.slaveIP.setText("")
         self.slavePort.setText("")
         self.label3.setText("")
         self.srvName.setText("")






if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = App()
     sys.exit(app.exec_())

