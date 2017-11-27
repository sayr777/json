import serial
import sys
import os
import time
import sqlite3
import mercury as m
sys.path.insert(0, "..")
from opcua import ua, Server

if __name__ == "__main__":

     serverSlave=''
     portSlave=0

     netAdr=[]
     unitName=[]
     
     sNum=[]
     EnT0=[]  
     EnT1=[]   
     EnT2=[]   
     EnT3=[]  
     EnT4=[]   
     Amper=[] 
     Volt=[] 
     P=[] 
     PQ=[] 
     PS=[] 
     Cos=[]
     Freq=[] 
     Angle=[]     
     Err1=[]       
     Err2=[]  

 
     
     idServ=sys.argv[1]
     connDb = sqlite3.connect(sys.argv[2])
     pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
 
    # idServ=str('68')
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



             
     cursor.execute("select netAdr,serNum from  master_mercury230 where serverId = "+ idServ)
     dt=cursor.fetchall()
     units=len(dt)

     for i in range(0,len(dt)):

         netAdr.append(i)
         unitName.append(i)
         sNum.append(i)
         EnT0.append(i) 
         EnT1.append(i)   
         EnT2.append(i)  
         EnT3.append(i) 
         EnT4.append(i)  
         Amper.append(i) 
         Volt.append(i)
         P.append(i)
         PQ.append(i) 
         PS.append(i) 
         Cos.append(i)
         Freq.append(i)
         Angle.append(i)     
         Err1.append(i)       
         Err2.append(i)
         
         netAdr[i]= dt[i][0]
         unitName[i]=objects.add_object(idx,dt[i][1])
         
         
         sNum[i]= unitName[i].add_variable(idx, "SerialNumber",0)  
         EnT0[i]= unitName[i].add_variable(idx, "Energy_0", [0,0,0,0])  
         EnT1[i]= unitName[i].add_variable(idx, "Energy_1", [0,0,0,0])  
         EnT2[i]= unitName[i].add_variable(idx, "Energy_2", [0,0,0,0])  
         EnT3[i]= unitName[i].add_variable(idx, "Energy_3", [0,0,0,0])  
         EnT4[i]= unitName[i].add_variable(idx, "Energy_4", [0,0,0,0])  
     
         Amper[i]= unitName[i].add_variable(idx, "Amper", [0,0,0])
         Volt[i] = unitName[i].add_variable(idx, "Volt", [0,0,0])
         P[i]    = unitName[i].add_variable(idx, "Power_P", [0,0,0,0])
         PQ[i]   = unitName[i].add_variable(idx, "Power_Q", [0,0,0,0])
         PS[i]   = unitName[i].add_variable(idx, "Power_S", [0,0,0,0])
         Cos[i]  = unitName[i].add_variable(idx, "Cos_F", [0,0,0,0])
         Freq[i] = unitName[i].add_variable(idx, "Freq", 0)
         Angle[i]= unitName[i].add_variable(idx, "Angle", [0,0,0])    
         Err1[i] = unitName[i].add_variable(idx, "ErrConnect", 0 )       
         Err2[i] = unitName[i].add_variable(idx, "ErrOpenChanel", 0 ) 




     serialPort = serial.Serial(port=serialPort, baudrate=int(ttySpeed), timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
     server.start()
    
     try:
         while True:
                 for i in range(units):
                     try:
                        
                         Err1[i].set_value(0)
                         Err2[i].set_value(0)
                         if(m.getConnect(netAdr[i],serialPort ) == 1):
                             Err1[i].set_value(1)
                             
                             if(m.sndOpCh(netAdr[i],serialPort) == 1):
                                 Err2[i].set_value(1)
                                 sNum[i].set_value(m.getSN(netAdr[i],serialPort))
             
                                 EnT0[i].set_value(m.getEn0(netAdr[i],serialPort))
                                 EnT1[i].set_value(m.getEn1(netAdr[i],serialPort))
                                 EnT2[i].set_value(m.getEn2(netAdr[i],serialPort))
                                 EnT3[i].set_value(m.getEn3(netAdr[i],serialPort))
                                 EnT4[i].set_value(m.getEn4(netAdr[i],serialPort))
                                 P[i].set_value(m.getP(netAdr[i],serialPort))
                                 PQ[i].set_value(m.getPQ(netAdr[i],serialPort))
                                 PS[i].set_value(m.getPS(netAdr[i],serialPort))
                                 Cos[i].set_value(m.getCosF(netAdr[i],serialPort))
                                 Freq[i].set_value(m.getFreq(netAdr[i],serialPort))
                                 Amper[i].set_value(m.getI(netAdr[i],serialPort))
                                 Volt[i].set_value(m.getU(netAdr[i],serialPort))
                                 Angle[i].set_value(m.getAngle(netAdr[i],serialPort))                                        
                             else:
                                 Err2[i].set_value(0)
                                 #print("Open Error")
                     
                         else:    
                             Err1[i].set_value(0) 
                             #print("Connect Error")


                     except Exception as e:
                         print ('Oops -----',e)
                         Err1[i].set_value(0)
                         Err2[i].set_value(0) 
                     time.sleep(float(timeOut))
     finally:
         serialPort.close()
         server.stop()





