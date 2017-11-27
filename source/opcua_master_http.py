
import sys
import time
import logging
import gc
import os
import sqlite3
import requests
from datetime import datetime
#from requests.auth import HTTPBasicAuth

from requests.packages import urllib3
urllib3.disable_warnings()
import threading
from opcua import ua, Server
sys.path.insert(0, "..")

def httpReq(adr,user,password,typeValue):
     gc.collect()
     if(typeValue=='int'):
         try:
             response = requests.get(adr, auth=(user,password), timeout=5,verify=False)
             if(response.status_code == 200):
                 r = [int(item) for item in response.text.split(',')]
             else:    
                 r=0
             gc.collect()
         except Exception as e:
        # print(e)
             r=0
   
     if(typeValue=='string'):
         try:
             response = requests.get(adr, auth=(user,password), timeout=5)
             if(response.status_code == 200):
                 r = response.text
             else:    
                 r=0
             gc.collect()
         except Exception as e:
        # print(e)
             r=0
     return r



if __name__ == "__main__":

     serverSlave=''
     portSlave=0

     reg=[]
     host=[]
     login=[]
     password=[]
     dataRIR=[]
     unitName=[]
     param=[]
     paramValue=[]
     valueType=[]
     units=0

     try:

         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])

        # idServ=str('70')
        # connDb = sqlite3.connect('f:\scadapy\config\db\srvDb.db')
         cursor = connDb.cursor()


         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             serialPort=row[2]
             ttySpeed=row[3]
             timeOut=row[4]   


         server = Server()
         server.set_endpoint("opc.tcp://"+serverSlave+":"+portSlave+"/srv/")
         server.set_server_name("Server")
         server.load_certificate(pathFolder+"server_cert.der")
         server.load_private_key(pathFolder+"server_private_key.pem")
         uri = "http://opcua.server.ru"
         idx = server.register_namespace(uri)
         objects = server.get_objects_node()



             
         cursor.execute("select ip,reg,toAdr,fromCount,comment,login,password from  master_http where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)

         for i in range(0,len(dt)):

             reg.append(i)
             host.append(i)
             login.append(i)
             password.append(i)             
             unitName.append(i)
             param.append(i)
             valueType.append(i)
             

             
             host[i]       =  dt[i][0]
             reg[i]        =  dt[i][1]
             valueType[i]  =  dt[i][2]    
             login[i]      =  dt[i][5]
             password[i]   =  dt[i][6] 
             unitName[i]=objects.add_object(idx,dt[i][4])
             paramValue=[]
             c=0
             for c in range(0,int(dt[i][3]) ):
                 paramValue.append(c)
                 paramValue[c]=0
                 c+=1
             param[i]= unitName[i].add_variable(idx,dt[i][1],paramValue)  
             i+=1
 
         server.start()
     except Exception as e:
         print (e)

     try:
         while True:
             i=0
             for i in range(units):
                     try:
                         try:
                             dataRIR=httpReq(host[i],login[i],password[i], valueType[i])
                             param[i].set_value(dataRIR)
                             print(host[i],'---', dataRIR)
                             dataRIR=None
                             gc.collect()
                         except Exception as e:

                             dataRIR=None
                             gc.collect()
                     except Exception as e:
                         pass
                     time.sleep(float(timeOut))
                     gc.collect()
     finally:
         server.stop()





