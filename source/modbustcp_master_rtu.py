
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
     units=0
     try:

         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])

         #idServ=str('66')
         #connDb = sqlite3.connect('D:\scadapy\windows\config\db\srvDb.db')
         cursor = connDb.cursor()


         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             serialPort=row[2]
             ttySpeed=row[3]
             timeOut=row[4]

         cursor.execute("select adrRtu,reg,fromAdr,fromCount,toAdr from  master_modbusRTU where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             rtuAddress.append(i)
             reg.append(i)
             startAdr.append(i)
             rangeAdr.append(i)
             setFrom.append(i)
             rtuAddress[i] =  dt[i][0]
             reg[i]        =  dt[i][1]
             startAdr[i]   =  dt[i][2]
             rangeAdr[i]   =  dt[i][3]
             setFrom[i]    =  dt[i][4]
             i+=1

         for c in range(0,1000 ):
             dataRIR.append(c)
             dataRDI.append(c)
             dataRC.append(c)
             dataRHR.append(c)
             c+=1

         server = modbus_tcp.TcpServer(address=serverSlave, port=int(portSlave) )
         server.start()
         slave = server.add_slave(1)

         slave.add_block('0', cst.COILS, 0, 1000)
         slave.add_block('1', cst.DISCRETE_INPUTS, 0, 1000)
         slave.add_block('2', cst.ANALOG_INPUTS, 0, 1000)
         slave.add_block('3', cst.HOLDING_REGISTERS, 0, 1000)


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


                         slave.set_values('2', int(setFrom[i]), dataRIR)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()

                         print('rtu' , rtuAddress[i],'READ_INPUT_REGISTERS',dataRIR)
                         dataRIR=None
                         gc.collect()

                     except Exception as e:
                         print ('rtu' , rtuAddress[i],'READ_INPUT_REGISTERS','Fail to connect' ,e)
                         slave.set_values('2', int(setFrom[i]), dataRIR)
                         dataRIR=None
                         gc.collect()


                 if(reg[i] == 'READ_DISCRETE_INPUTS'):

                     try:
                         dataRDI= master.execute(int(rtuAddress[i]), cst.READ_DISCRETE_INPUTS, int(startAdr[i]), int(rangeAdr[i])  )
                         slave.set_values('1', int(setFrom[i]), dataRDI)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         gc.collect()
                         dataRDI=None
                         print(  'rtu' , rtuAddress[i],'READ_DISCRETE_INPUTS',dataRDI)
                     except:

                         print ('rtu' , rtuAddress[i],'READ_DISCRETE_INPUTS','Fail to connect' ,dataRDI,len(dataRDI))
                         slave.set_values('1', int(setFrom[i]), dataRDI)
                         gc.collect()
                         dataRDI=None


                 if(reg[i] == 'READ_COILS'):

                     try:
                         dataRC= master.execute(int(rtuAddress[i]), cst.READ_COILS, int(startAdr[i]), int(rangeAdr[i])  )
                         slave.set_values('0', int(setFrom[i]), dataRC)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         gc.collect()

                         print ( 'rtu' , rtuAddress[i],'READ_COILS',dataRC)
                         dataRC=None
                     except:

                         slave.set_values('0', int(setFrom[i]), dataRC)
                         print( 'rtu' , rtuAddress[i],'READ_COILS','Fail to connect',dataRC)
                         gc.collect()
                         dataRC=None

                 if(reg[i] == 'READ_HOLDING_REGISTERS'):

                     try:
                         dataRHR= master.execute(int(rtuAddress[i]), cst.READ_HOLDING_REGISTERS, int(startAdr[i]), int(rangeAdr[i])  )
                         slave.set_values('3', int(setFrom[i]), dataRHR)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         print ( 'rtu' ,rtuAddress[i],'READ_HOLDING_REGISTERS',dataRHR)
                         gc.collect()
                         dataRHR=None

                     except:

                         slave.set_values('3', int(setFrom[i]), dataRHR)
                         print ('rtu ', rtuAddress[i],'READ_HOLDING_REGISTERS','Fail to connect',dataRHR)
                         gc.collect()
                         dataRHR=None

                 time.sleep(float(timeOut))
                 gc.collect()

     except modbus_tk.modbus.ModbusError as e:
         logger.error("%s- Code=%d" % (e, e.get_exception_code()))





