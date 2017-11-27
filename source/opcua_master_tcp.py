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
     host=[]
     master=[]
     port=[]
     unitName=[]
     comment=[]
     param=[]     
     units=0
     try:

         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])

       #  idServ=str('71')
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
         
         
                      
         cursor.execute("select adrRtu,reg,fromAdr,fromCount,toAdr,ip,port,comment from  master_modbusTCP where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             rtuAddress.append(i)
             reg.append(i)
             startAdr.append(i)
             rangeAdr.append(i)
             setFrom.append(i)
             host.append(i)
             master.append(i)
             port.append(i)
             unitName.append(i)
             comment.append(i)
             param.append(i)             
             rtuAddress[i] =  dt[i][0]
             reg[i]        =  dt[i][1]
             startAdr[i]   =  dt[i][2]
             rangeAdr[i]   =  dt[i][3]
             setFrom[i]    =  dt[i][4]
             host[i]       =  dt[i][5]
             port[i]       =  dt[i][6]
             comment[i]    =  dt[i][7]
             unitName[i]=objects.add_object(idx,dt[i][7])

             paramValue=[]
             c=0
             for c in range(0,int(dt[i][3]) ):
                 paramValue.append(c)
                 paramValue[c]=0
                 c+=1
             
             param[i]= unitName[i].add_variable(idx,'Val',paramValue)  

             
             try:
                 master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                 master[i].set_timeout(1.0)
             except Exception as e:
                 pass

             i+=1

         for c in range(0,1000 ):
             dataRIR.append(c)
             dataRDI.append(c)
             dataRC.append(c)
             dataRHR.append(c)
             c+=1




         server.start()
   
     except IOError as e:
         print ("I/O error({0}): {1}".format(e.errno, e.strerror))

     try:

         while True:
             i=0
             for i in range(units):
                 if(reg[i] == 'READ_INPUT_REGISTERS'):

                     try:
                         try:
                             dataRIR= master[i].execute(int(rtuAddress[i]), cst.READ_INPUT_REGISTERS, int(startAdr[i]), int(rangeAdr[i])  )
                             param[i].set_value(dataRIR)
                             print(comment[i] ,host[i],port[i], rtuAddress[i],'READ_INPUT_REGISTERS',dataRIR)
                             dataRIR=None
                             gc.collect()
                         except Exception as e:
                         #    slave.set_values('2', int(setFrom[i]), dataRIR)
                             dataRIR=None
                             gc.collect()
                             master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                             master[i].set_timeout(3.0)
                     except Exception as e:
                         pass

                 if(reg[i] == 'READ_DISCRETE_INPUTS'):
                     try:

                         try:
                             dataRDI= master[i].execute(int(rtuAddress[i]), cst.READ_DISCRETE_INPUTS, int(startAdr[i]), int(rangeAdr[i])  )
                             param[i].set_value(dataRDI)

                             print(  comment[i] ,host[i],port[i], rtuAddress[i],'READ_DISCRETE_INPUTS',dataRDI)
                             dataRDI=None
                             gc.collect()
                         except Exception as e:
                             print (comment[i] ,host[i],port[i], rtuAddress[i],'READ_DISCRETE_INPUTS','Fail to connect' )

                             gc.collect()
                             dataRDI=None
                             master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                             master[i].set_timeout(3.0)
                     except Exception as e:
                         pass

                 if(reg[i] == 'READ_COILS'):
                     try:
                         try:
                             dataRC= master[i].execute(int(rtuAddress[i]), cst.READ_COILS, int(startAdr[i]), int(rangeAdr[i])  )
                             param[i].set_value(dataRC)

                             print (comment[i] ,host[i],port[i], rtuAddress[i],'READ_COILS',dataRC)
                             dataRC=None
                             gc.collect()
                         except Exception as e:

                             print( comment[i] ,host[i],port[i], rtuAddress[i],'READ_COILS','Fail to connect')
                             gc.collect()
                             dataRC=None
                             master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                             master[i].set_timeout(3.0)
                     except Exception as e:
                         pass

                 if(reg[i] == 'READ_HOLDING_REGISTERS'):
                     try:
                         try:
                             dataRHR= master[i].execute(int(rtuAddress[i]), cst.READ_HOLDING_REGISTERS, int(startAdr[i]), int(rangeAdr[i])  )
                             param[i].set_value(dataRHR)

                             print ( comment[i],host[i],port[i],rtuAddress[i],'READ_HOLDING_REGISTERS',dataRHR)
                             dataRHR=None
                             gc.collect()
                         except Exception as e:

                             print (comment[i],host[i],port[i],rtuAddress[i],'READ_HOLDING_REGISTERS','Fail to connect')
                             gc.collect()
                             dataRHR=None
                             master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                             master[i].set_timeout(3.0)
                     except Exception as e:
                         pass
            # print(timeOut)
                 time.sleep(float(timeOut))
             gc.collect()

     except modbus_tk.modbus.ModbusError as e:
         logger.error("%s- Code=%d" % (e, e.get_exception_code()))





