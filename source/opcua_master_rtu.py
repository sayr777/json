
import sys
import time
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from modbus_tk import modbus_rtu
import serial
logger = modbus_tk.utils.create_logger("console")
import gc
import os
import sqlite3
from opcua import ua, Server
sys.path.insert(0, "..")
if __name__ == "__main__":

     serverSlave=''
     portSlave=0

     reg=[]
     startAdr=[]
     rangeAdr=[]
     setFrom=[]
     rtuAddress=[]
     dataRIR=[]
     dataRDI=[]
     dataRC=[]
     dataRHR=[]
     unitName=[]
     comment=[]
     param=[]       
     units=0
     try:

         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])

         #idServ=str('91')
       #  connDb = sqlite3.connect('f:\scadapy\config\db\srvDb.db')
         cursor = connDb.cursor()


         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             serialPort=row[2]
             ttySpeed=row[3]      
             timeOut=row[4]    

         server = Server()
         server.set_endpoint("opc.tcp://"+serverSlave+":"+portSlave+"/")
         server.set_server_name("Server")
         server.load_certificate(pathFolder+"server_cert.der")
         server.load_private_key(pathFolder+"server_private_key.pem")
         uri = "http://server"
         idx = server.register_namespace(uri)
         objects = server.get_objects_node()


         cursor.execute("select adrRtu,reg,fromAdr,fromCount,toAdr,comment from  master_modbusRTU where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             rtuAddress.append(i)
             reg.append(i)
             startAdr.append(i)
             rangeAdr.append(i)
             comment.append(i)
             unitName.append(i)
             param.append(i)
            # setFrom.append(i)
             rtuAddress[i] =  dt[i][0]
             reg[i]        =  dt[i][1]
             startAdr[i]   =  dt[i][2]
             rangeAdr[i]   =  dt[i][3]
            # setFrom[i]    =  dt[i][4]
             comment[i]    =  dt[i][5]
             unitName[i]=objects.add_object(idx,dt[i][5])
             paramValue=[]
             c=0
             for c in range(0,int(dt[i][3]) ):
                 paramValue.append(c)
                 paramValue[c]=0
                 c+=1
             
             param[i]= unitName[i].add_variable(idx,'Val',paramValue)  

             i+=1

         for c in range(0,1000 ):
             dataRIR.append(c)
             dataRDI.append(c)
             dataRC.append(c)
             dataRHR.append(c)
             c+=1

         server.start()

         serialPort=serial.Serial(port=serialPort, baudrate=int(ttySpeed), bytesize=8, parity='N', stopbits=1, xonxoff=0)

         master = modbus_rtu.RtuMaster( serialPort )
         master.set_timeout(1.0)

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
                         dataRIR= master.execute(int(rtuAddress[i]), cst.READ_INPUT_REGISTERS, int(startAdr[i]), int(rangeAdr[i])  )

                         param[i].set_value(dataRIR)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()

                         print(comment[i], rtuAddress[i],'READ_INPUT_REGISTERS',dataRIR)
                         dataRIR=None
                         gc.collect()

                     except:

                         print (comment[i], rtuAddress[i],'READ_INPUT_REGISTERS','Fail to connect' )
                         dataRIR=None
                         gc.collect()


                 if(reg[i] == 'READ_DISCRETE_INPUTS'):

                     try:
                         dataRDI= master.execute(int(rtuAddress[i]), cst.READ_DISCRETE_INPUTS, int(startAdr[i]), int(rangeAdr[i])  )

                         param[i].set_value(dataRDI)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         gc.collect()
                         dataRDI=None
                         print( comment[i] , rtuAddress[i],'READ_DISCRETE_INPUTS',dataRDI)
                     except:

                         print (comment[i], rtuAddress[i],'READ_DISCRETE_INPUTS','Fail to connect')

                         gc.collect()
                         dataRDI=None


                 if(reg[i] == 'READ_COILS'):

                     try:
                         dataRC= master.execute(int(rtuAddress[i]), cst.READ_COILS, int(startAdr[i]), int(rangeAdr[i])  )

                         param[i].set_value(dataRC)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         gc.collect()

                         print ( comment[i], rtuAddress[i],'READ_COILS',dataRC)
                         dataRC=None
                     except:

                         print( comment[i] , rtuAddress[i],'READ_COILS','Fail to connect')
                         gc.collect()
                         dataRC=None

                 if(reg[i] == 'READ_HOLDING_REGISTERS'):

                     try:
                         dataRHR= master.execute(int(rtuAddress[i]), cst.READ_HOLDING_REGISTERS, int(startAdr[i]), int(rangeAdr[i])  )

                         param[i].set_value(dataRHR)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         print ( comment[i],rtuAddress[i],'READ_HOLDING_REGISTERS',dataRHR)
                         gc.collect()
                         dataRHR=None

                     except:

                         print (comment[i], rtuAddress[i],'READ_HOLDING_REGISTERS','Fail to connect')
                         gc.collect()
                         dataRHR=None

                 time.sleep(float(timeOut))
                 gc.collect()

     except modbus_tk.modbus.ModbusError as e:
         logger.error("%s- Code=%d" % (e, e.get_exception_code()))





