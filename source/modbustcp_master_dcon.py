import sys
import time
#import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

import serial

import sqlite3


if __name__ == "__main__":

     serverSlave=''
     portSlave=0
     adamAddress=[]
     unitName=[]
     model=[] 
     setFrom=[]
     comment=[]
     units=0
     dataIn=''
     
     #pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
     idServ=sys.argv[1]
     connDb = sqlite3.connect(sys.argv[2])

    # idServ=str('72')
    # connDb = sqlite3.connect('f:\scadapy\config\db\srvDb.db')
     
     
     
     try:
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             ttyPort=row[2]
             ttySpeed=row[3]
             timeOut=row[4]   
        
         cursor.execute("select adrRtu,model,toAdr,comment from  master_dcon where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             adamAddress.append(i)
             setFrom.append(i)
             model.append(i)
             comment.append(i)

             adamAddress[i] =  dt[i][0]
             model[i]       =  dt[i][1]
             setFrom[i]     =  dt[i][2]
             comment[i]     =  dt[i][3]

         server = modbus_tcp.TcpServer(address=serverSlave, port=int(portSlave) )
         server.start()
         slave = server.add_slave(1)

         slave.add_block('0', cst.COILS, 0, 1000)
         slave.add_block('1', cst.DISCRETE_INPUTS, 0, 1000)
         slave.add_block('2', cst.ANALOG_INPUTS, 0, 1000)
         slave.add_block('3', cst.HOLDING_REGISTERS, 0, 1000)

         serialPort=serial.Serial(port=ttyPort, baudrate=int(ttySpeed), bytesize=8, parity='N', stopbits=1, xonxoff=0,timeout=1)
     except Exception as e:
         print (e)
     try:
         print ('Starting server...')
         

         for i in range(0,units):
##########  4050 init
                 if(model[i] == '4050'):
                     try:
                         
                         sendCom='$'+ adamAddress[i]+'6\r'
                         serialPort.write(sendCom.encode())
                         dataIn = serialPort.read(8)
                         
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         
                         if(chr(dataIn[0])=='!'):
                             
                             byteDI   = str(bin(int('0x'+chr(dataIn[3])+chr(dataIn[4]),16))[2:].zfill(8))
                             byteCoil = str(bin(int('0x'+chr(dataIn[1])+chr(dataIn[2]),16))[2:].zfill(8))

                             for c in range(0,8):
                                 slave.set_values('1', int(setFrom[i])+c, int(byteDI[c]) )
                                 slave.set_values('0', int(setFrom[i])+c, int(byteCoil[c]) )
                                 c+=1
                             print ('dcon' , 'Discret', byteDI, 'Coils',byteCoil ,dataIn)                
                     except Exception as e:
                         print ('dcon' ,'Bad answer','Fail to connect',e)
                     i+=1


#####################################################################################################                      
         while True:
             i=0
             for i in range(units):
                 if(model[i] == '4050'):
                     try:
                         getCoils = slave.get_values('0', int(setFrom[i]), 8)
                         xHi= (int(getCoils[0])<<3)+(int(getCoils[1])<<2)+(int(getCoils[2])<<1)+int(getCoils[3])
                         xLow=(int(getCoils[4])<<3)+(int(getCoils[5])<<2)+(int(getCoils[6])<<1)+int(getCoils[7]) 
                         strSend=str(hex(xHi)).upper()[2:] + str(hex(xLow)).upper()[2:]
                         sendCom = '#'+adamAddress[i]+'00'+ strSend+'\r'

                         serialPort.write(sendCom.encode())
                         dataCom = serialPort.read(2)
                       
                         sendCom='$'+ adamAddress[i]+'6\r'
                         serialPort.write(sendCom.encode())
                         dataIn = serialPort.read(8)
                         serialPort.flushInput()
                         serialPort.flushOutput()
                         serialPort.flush()
                         if(chr(dataIn[0])=='!'):
                             
                             byteDI   = str(bin(int('0x'+chr(dataIn[3])+chr(dataIn[4]),16))[2:].zfill(8))
                             byteCoil = str(bin(int('0x'+chr(dataIn[1])+chr(dataIn[2]),16))[2:].zfill(8))

                             for c in range(0,8):
                                 slave.set_values('1', int(setFrom[i])+c, int(byteDI[c]) )
                                 slave.set_values('0', int(setFrom[i])+c, int(byteCoil[c]) )
                                 c+=1
                             print ('dcon',setFrom[i], 'Discret', byteDI, 'Coils',byteCoil ,dataIn)
                     except Exception as e:
                         print ('dcon' ,'Bad answer','Fail to connect',e)
#####################################################################################################                         
                 i+=1
                 time.sleep(float(timeOut))
     except modbus_tk.modbus.ModbusError as e:
         print ('Error ',e)


