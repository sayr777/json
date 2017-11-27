#!/usr/bin/python3.5
import sys
import os
from PyQt5.QtGui import  QIcon,QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QMessageBox,QApplication,QMainWindow, QAction, qApp,QFileDialog,QTreeView,QTreeWidgetItem,QLineEdit,QLabel,QComboBox,QFrame)
from PyQt5.QtWidgets import (QTreeWidgetItemIterator,QTableWidget,QTableWidgetItem,QAbstractItemView,QInputDialog)

from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QItemSelectionModel
import sqlite3
#import srvconf



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

         self.srvList=["","opcUA","modbusTCP"]

         if(os.name=='nt'):

             self.appPath=os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
             self.imgPath=self.appPath+"img\\"
             self.dbPath=self.appPath+"db\\webDb.db"
             #import self.appPath+srvconf

         else:
             self.appPath=os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
             self.imgPath=self.appPath+"img/"
             self.dbPath=self.appPath+"db/webDb.db"


         self.versionPr='ScadaPy Web JSON Сервер v.3.14'
         self.setGeometry(300, 100, 1500, 820)
         self.setWindowTitle(self.versionPr)
         self.setWindowIcon(QIcon( self.imgPath+'Globe.png'))
         self.h=self.frameGeometry().height()
         self.w=self.frameGeometry().width()
         self.setStyleSheet("background-color: #FFF8E7;")

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
         self.label2.setText("Http IP address")
         self.slaveIP = QLineEdit(self)
         self.slaveIP.setToolTip('Пример: 192.168.0.111')
         self.slaveIP.move(550, 120)
         self.slaveIP.setFont(font)
         self.slaveIP.resize(300,25)


         self.label2=QLabel(self)
         self.label2.setFont(font)
         self.label2.move(400, 150)
         self.label2.resize(140,25)
         self.label2.setText("Http Port")
         self.slavePort = QLineEdit(self)
         self.slavePort.setToolTip('Пример : 8080')
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

         self.label8=QLabel(self)
         self.label8.setFont(font)
         self.label8.move(400, 180)
         self.label8.resize(140,25)
         self.label8.setText("Login")
         self.serverLogin = QLineEdit(self)
         self.serverLogin.setToolTip('Имя пользователя')
         self.serverLogin.move(550, 180)
         self.serverLogin.setFont(font)
         self.serverLogin.resize(100,25)

         self.label9=QLabel(self)
         self.label9.setFont(font)
         self.label9.move(680, 180)
         self.label9.resize(140,25)
         self.label9.setText("Password")
         self.serverPassword = QLineEdit(self)
         self.serverPassword.setToolTip('Пароль')
         self.serverPassword.move(750, 180)
         self.serverPassword.setFont(font)
         self.serverPassword.resize(100,25)

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

         runConf = QAction(QIcon(self.imgPath+'app.png'), '&Запустить конфигуратор', self)
         runConf.setStatusTip('Запустить конфигуратор')
         runConf.triggered.connect(self.runConf)



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
         self.toolbar.addAction(runConf)



        # self.statusBar().showMessage('Загрузка данных')

         self.treeView = QTreeView(self)
         self.treeView.setFont(font)
         self.treeView.setObjectName("treeView")
         self.model = QStandardItemModel()
         self.treeView.setModel(self.model)
         self.treeView.setStyleSheet("background-color: white;")
         self.header = ['Название сервера']
         self.model.setHorizontalHeaderLabels(self.header)

         self.sqlLoad()
         self.treeView.clicked.connect(self.onClickItem)





         self.frameTable = QFrame(self)
         self.frameTable.setVisible(True)

         self.addRow = QPushButton(self.frameTable)
         self.addRow.setIcon(QIcon(self.imgPath+'add.png'))
         self.addRow.move(10, 10)
         self.addRow.resize(30,30)
         self.addRow.clicked.connect(self.addItemTree)

         self.saveTable = QPushButton(self.frameTable)
         self.saveTable.setIcon(QIcon(self.imgPath+'filesave.png'))
         self.saveTable.resize(30,30)
         self.saveTable.move(50, 10)
         self.saveTable.clicked.connect(self.saveData)


####################################################################

         self.treeTable = QTableWidget(self.frameTable)
         self.treeTable.setStyleSheet("background-color: white;")
         fontTable = QFont()
         fontTable.setPointSize(10)
         self.treeTable.setFont(fontTable)


 #        self.show()
         self.showMaximized()


    def addItemTree(self):
         items = ("modbus_tcp","opc_ua")
         item, okPressed = QInputDialog.getItem(self, "Добавить тип сервера","Тип:", items, 0, False)
         if okPressed and item:
             self.treeTable.insertRow(self.treeTable.rowCount())
             self.treeTable.setItem(self.treeTable.rowCount()-1, 0, QTableWidgetItem(item))

    def getData(self):
             self.treeTable.clear()
             self.treeTable.setColumnCount(10)
             #self.treeTable.setRowCount(1)
             self.treeTable.setHorizontalHeaderLabels(['Тип сервера','Имя переменной','Имя параметра','IP адрес', 'Порт','Логин','Пароль','Timeout','Адрес ячейки','Количество'])
             self.treeTable.resizeColumnsToContents()
             self.treeTable.setColumnWidth(0, 120)
             self.treeTable.setColumnWidth(1, 170)
             self.treeTable.setColumnWidth(2, 170)
             self.treeTable.setColumnWidth(3, 140)
             self.treeTable.setColumnWidth(4, 80)
             self.treeTable.setColumnWidth(5, 120)
             self.treeTable.setColumnWidth(6, 120)
             self.treeTable.setColumnWidth(7, 80)
             self.treeTable.setColumnWidth(8, 120)
             self.treeTable.setColumnWidth(9, 80)

             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select type,var,param,ip,port,login,password,t,regadr,regcount from  master where serverId = "+self.label00.text())
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
                 self.treeTable.setItem(i, 8, QTableWidgetItem(dt[i][8]))
                 self.treeTable.setItem(i, 9, QTableWidgetItem(dt[i][9]))


                 i+=1



    def saveData(self):
                 connDb = sqlite3.connect(self.dbPath)
                 cursor = connDb.cursor()
                 cursor.execute("delete from master where serverId= '"+self.label00.text()+"'" )
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
                                     len(self.treeTable.item(i,7).text()) > 0 and
                                     len(self.treeTable.item(i,8).text()) > 0 ):

                                 cursor.execute("INSERT INTO master(serverId,type,var,param,ip,port,login,password,t,regadr,regcount,valid)\
                                 VALUES('"+self.label00.text()+"',\
                                 '"+self.treeTable.item(i,0).text()+"',\
                                 '"+self.treeTable.item(i,1).text()+"',\
                                 '"+self.treeTable.item(i,2).text()+"',\
                                 '"+self.treeTable.item(i,3).text()+"',\
                                 '"+self.treeTable.item(i,4).text()+"',\
                                 '"+self.treeTable.item(i,5).text()+"',\
                                 '"+self.treeTable.item(i,6).text()+"',\
                                 '"+self.treeTable.item(i,7).text()+"',\
                                 '"+self.treeTable.item(i,8).text()+"',\
                                 '"+self.treeTable.item(i,9).text()+"',\
                                 1)" )
                                 connDb.commit()
                         except Exception as e:
                             print(e)
                             pass
                         i+=1
                 self.getData()



    def truePanel(self):
         self.getData()

    def onClickItem (self):
         self.treeTable.clear()
         self.treeTable.setRowCount(0)
         self.srvName.setText("")
         self.label00.setText("")
         self.slaveIP.setText("")
         self.slavePort.setText("")
         self.serverTimeout.setText("")
         self.serverLogin.setText("")
         self.serverPassword.setText("")
         
         try:
             self.slaveIP.setEnabled(True)
             self.slavePort.setEnabled(True)
             index_list =[i.data() for i in self.treeView.selectedIndexes()]
             s=index_list[0].split(':')
             self.srvName.setText(s[1])
             self.label00.setText(s[0])

             connDb = sqlite3.connect(self.dbPath)
             cursor = connDb.cursor()
             cursor.execute("select ip, port,timeout,login,password from  servers where id = "+s[0])
             dt=cursor.fetchone()
             self.slaveIP.setText(dt[0])
             self.slavePort.setText(dt[1])
             self.serverTimeout.setText(dt[2])
             self.serverLogin.setText(dt[3])
             self.serverPassword.setText(dt[4])
             self.truePanel()



         except Exception as e:
             index_list =[i.data() for i in self.treeView.selectedIndexes()]
             self.srvName.setText(index_list[0])
             self.slaveIP.setEnabled(False)
             self.slavePort.setEnabled(False)
             print(e)




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
         self.treeTable.setGeometry(QtCore.QRect(10, 50, self.w-270, self.h-320))
         self.frameTable.setGeometry(QtCore.QRect(350, 210, self.w-250, self.h-260))



    def sqlLoad(self):
         connDb = sqlite3.connect(self.dbPath)
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT name, id FROM servers where valid=1 ORDER BY id'):
             self.model.appendRow(QStandardItem(str(row[1])+":"+row[0]))

    def saveServer(self):
         self.treeTable.clear()

         connDb = sqlite3.connect(self.dbPath)
         cursor = connDb.cursor()
         if(len(self.label00.text())>0 and int(self.label00.text()) >0):
             if(len(self.srvName.text()) > 1):
                 connDb.execute("update servers set name ='"+self.srvName.text()+ "', ip = '"+self.slaveIP.text()+"', port = '"+self.slavePort.text()+"'\
                 ,timeout='"+self.serverTimeout.text()+"', login='"+self.serverLogin.text()+"',password='"+self.serverPassword.text()+"' where id = "+self.label00.text()+" ")
                 connDb.commit()
                 cursor.execute("select ip,port,timeout,login,password from  servers where id = "+self.label00.text())
                 dt=cursor.fetchone()
                 self.slaveIP.setText(dt[0])
                 self.slavePort.setText(dt[1])
                 self.serverTimeout.setText(dt[2])
                 self.serverLogin.setText(dt[3])
                 self.serverPassword.setText(dt[4])
                 
                 self.truePanel()
         else:
             try:
                 if(len(self.srvName.text()) > 1):
                     cursor.execute("INSERT INTO servers(name,valid)  VALUES( '"+self.srvName.text()+"',1)" )



                     connDb.commit()
             except Exception as e:
                 #print(e)
                 pass

         self.model.clear()
         self.model.setHorizontalHeaderLabels(self.header)
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT name, id FROM servers where valid=1 ORDER BY id'):
             self.model.appendRow(QStandardItem(str(row[1])+":"+row[0]))
       #  self.truePanel()

    def saveScr(self):

         try:
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

             f=open(pathFolder +'scr'+slash+'web_'+self.label00.text() + bat,'w')
             print(pathFolder +'scr'+slash+'web_'+self.label00.text() + bat)
             f.write(rem+'Скрипт создан в программе \''+self.versionPr+'\'\n')
             f.write(rem+'Сервер Web \''+self.srvName.text()+'\'\n')
             f.write(rem+'Http адрес \''+self.slaveIP.text()+'\'\n')
             f.write(rem+'Http порт \''+self.slavePort.text()+'\'\n')


             f.write(command+sys.executable+' '+pathFolder +'source'+slash+'websrv.py '+self.label00.text() +' '+pathFolder +'db'+slash+'webDb.db')
             f.close()
             ret = pathFolder +''+slash+'scr'+slash+'web_'+self.label00.text() + bat

         except Exception as e:
             print(e)

         return ret

    def runScr(self):

             if(os.name=='nt'):
                 os.system(self.saveScr())
             else:
                 os.system('chmod 777 '+self.saveScr())
                 os.system('xfce4-terminal --command=\'sudo '+self.saveScr()+'\'')


    def runConf(self):
         if(os.name=='nt'):

             self.appPath=os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
             os.system(sys.executable + " "+self.appPath +"srvconf.py")



         else:
             self.appPath=os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
             os.system(sys.executable + " "+self.appPath +"srvconf.py")





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
        # self.label3.setText("")
         self.srvName.setText("")






if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = App()
     sys.exit(app.exec_())

