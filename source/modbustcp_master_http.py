import sys
import time
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
logger = modbus_tk.utils.create_logger("console")
import gc
import os
import sqlite3
import requests
from datetime import datetime
import threading
#from requests.auth import HTTPBasicAuth

from requests.packages import urllib3
urllib3.disable_warnings()




def httpReq(adr,user,password):
     gc.collect()
     try:
         
         response = requests.get(adr, auth=(user,password), timeout=5,verify=False)
         if(response.status_code == 200):
             r = [int(item) for item in response.text.split(',')]
         else:    
             r=0
         gc.collect()
     except Exception as e:
         #print(e)
         r=0
     return r



if __name__ == "__main__":

     serverSlave=''
     portSlave=0

     reg=[]
     startAdr=[]
     rangeAdr=[]
     setFrom=[]
     host=[]
     comment=[]
     login=[]
     password=[]
     dataRIR=[]
     dataRDI=[]
     dataRC=[]
     dataRHR=[]
     units=0

     try:

         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])

       #idServ=str('69')
       # connDb = sqlite3.connect('f:\scadapy\config\db\srvDb.db')
         cursor = connDb.cursor()


         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             serialPort=row[2]
             ttySpeed=row[3]
             timeOut=row[4]   

             
         cursor.execute("select ip,reg,toAdr,fromCount,comment,login,password from  master_http where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             reg.append(i)
             rangeAdr.append(i)
             setFrom.append(i)
             host.append(i)
             comment.append(i)
             login.append(i)
             password.append(i)             
             
             host[i]       =  dt[i][0]
             reg[i]        =  dt[i][1]             
             setFrom[i]    =  dt[i][2]
             rangeAdr[i]   =  dt[i][3]
             comment[i]    =  dt[i][4]
             login[i]      =  dt[i][5]
             password[i]   =  dt[i][6]             
             i+=1

 
         server = modbus_tcp.TcpServer(address=serverSlave, port=int(portSlave) )
         server.start()
         slave = server.add_slave(1)

         slave.add_block('0', cst.COILS, 0, 1000)
         slave.add_block('1', cst.DISCRETE_INPUTS, 0, 1000)
         slave.add_block('2', cst.ANALOG_INPUTS, 0, 1000)
         slave.add_block('3', cst.HOLDING_REGISTERS, 0, 1000)

     except IOError as e:
         print ("I/O error({0}): {1}".format(e.errno, e.strerror))

     try:
         print( 'Starting server...')
         time.sleep(3.0)
         while True:
             i=0
             for i in range(units):
                 if(reg[i] == 'READ_INPUT_REGISTERS'):

                     try:
                         try:
                             dataRIR=httpReq(host[i],login[i],password[i])
                             slave.set_values('2', int(setFrom[i]), dataRIR)
                             print(host[i],'READ_INPUT_REGISTERS', dataRIR)
                             dataRIR=None
                             gc.collect()
                         except Exception as e:
                             slave.set_values('2', int(setFrom[i]), dataRIR)
                             dataRIR=None
                             gc.collect()
                     except Exception as e:
                         pass

                 if(reg[i] == 'READ_DISCRETE_INPUTS'):
                     try:

                         try:
                             dataRDI=httpReq(host[i],login[i],password[i])

                             slave.set_values('1', int(setFrom[i]), dataRDI)
                             print(host[i],'READ_DISCRETE_INPUTS',dataRDI)
                             dataRDI=None
                             gc.collect()
                         except Exception as e:
                             print (host[i],'READ_DISCRETE_INPUTS','Fail to connect' )
                             slave.set_values('1', int(setFrom[i]), dataRDI)
                             gc.collect()
                             dataRDI=None
                     except Exception as e:
                         pass

                 if(reg[i] == 'READ_COILS'):
                     try:
                         try:
                             dataRC= httpReq(host[i],login[i],password[i])
                             slave.set_values('0', int(setFrom[i]), dataRC)
                             print ( host[i],'READ_COILS',dataRC)
                             dataRC=None
                             gc.collect()
                         except Exception as e:
                             slave.set_values('0', int(setFrom[i]), dataRC)
                             print( host[i],'READ_COILS','Fail to connect')
                             gc.collect()
                             dataRC=None

                     except Exception as e:
                         pass

                 if(reg[i] == 'READ_HOLDING_REGISTERS'):
                     try:
                         try:
                             dataRHR=httpReq(host[i],login[i],password[i])
                             slave.set_values('3', int(setFrom[i]), dataRHR)
                             print ( host[i],'READ_HOLDING_REGISTERS',dataRHR)
                             dataRHR=None
                             gc.collect()
                         except Exception as e:
                             slave.set_values('3', int(setFrom[i]), dataRHR)
                             print (host[i],'READ_HOLDING_REGISTERS','Fail to connect')
                             gc.collect()
                             dataRHR=None

                     except Exception as e:
                         pass

                 time.sleep(float(timeOut))
                 gc.collect()

     except modbus_tk.modbus.ModbusError as e:
         logger.error("%s- Code=%d" % (e, e.get_exception_code()))





