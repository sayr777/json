
import sys
import time
#import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import os
import serial

import sqlite3
from opcua import ua, Server
sys.path.insert(0, "..")

if __name__ == "__main__":

     serverSlave=''
     portSlave=0
     adamAddress=[]
     unitName=[]
     model=[] 
     setFrom=[]
     comment=[]
     DI=[]
     DO=[]
     units=0
     dataIn=''
     coil=[]
     pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
     idServ=sys.argv[1]
     connDb = sqlite3.connect(sys.argv[2])

     #idServ=str('73')
    # connDb = sqlite3.connect('f:\scadapy\config\db\srvDb.db')
     
     
     
     try:
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             ttyPort=row[2]
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
                  
        
         cursor.execute("select adrRtu,model,toAdr,comment from  master_dcon where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             adamAddress.append(i)
             setFrom.append(i)
             model.append(i)
             comment.append(i)
             unitName.append(i)
             DI.append(i)
             DO.append(i)
             

             adamAddress[i] =  dt[i][0]
             model[i]       =  dt[i][1]
             setFrom[i]     =  dt[i][2]
             comment[i]     =  dt[i][3]
             unitName[i]=objects.add_object(idx,dt[i][3])

             DI[i]= unitName[i].add_variable(idx,'DI',[0,0,0,0,0,0,0,0])  
             DO[i]= unitName[i].add_variable(idx,'DO',[0,0,0,0,0,0,0,0]) 
             DO[i].set_writable()

             i+=1

         server.start()
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
                             DI[i].set_value([int(item) for item in byteDI])
                             DO[i].set_value([int(item) for item in byteCoil])

                             print ('dcon' , 'Discret', byteDI, 'Coils',byteCoil ,dataIn)                
                     except Exception as e:
                         print ('dcon' ,'Bad answer','Fail to connect',e)
                     i+=1


#####################################################################################################                      
         while True:
             
             for i in range(0,units):
                 if(model[i] == '4050'):
                     try:
                         coil=DO[i].get_value()

                         xHi= (int(coil[0])<<3)+(int(coil[1])<<2)+(int(coil[2])<<1)+int(coil[3])
                         xLow=(int(coil[4])<<3)+(int(coil[5])<<2)+(int(coil[6])<<1)+int(coil[7]) 
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

                             DI[i].set_value([int(item) for item in byteDI])
                             DO[i].set_value([int(item) for item in byteCoil])
                             print ('dcon', 'Discret', byteDI, 'Coils',byteCoil ,dataIn)
                     except Exception as e:
                         print ('dcon' ,'Bad answer','Fail to connect',e)
#####################################################################################################                         
                 i+=1
                 time.sleep(float(timeOut))
     except Exception as e:
         print ('Error ',e)


