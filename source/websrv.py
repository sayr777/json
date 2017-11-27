
import sys
import time
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
#logger = modbus_tk.utils.create_logger("console")
import gc
import os
import sqlite3
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
#import logging
import json
import base64
from opcua import ua, Client
import ssl
from dateutil import parser
from datetime import datetime
from enum import Enum, IntEnum
import uuid

class S(BaseHTTPRequestHandler):


     def _set_response(self):
         self.send_response(200)
         self.send_header('Content-type', 'text/html')
         self.end_headers()

     def do_HEAD(self):
         self.send_response(200)
         self.send_header('Content-type', 'text/html')
         self.send_header('Access-Control-Allow-Origin', '*')
         self.send_header('Access-Control-Allow-Credentials', 'true')
         self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
         self.send_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
         self.send_header("Access-Control-Allow-Headers", "Authorization")
         self.send_header("Access-Control-Allow-Headers","X-Accept-Charset,X-Accept,Content-Type,Credentials")
         self.end_headers()

     def do_AUTHHEAD(self):
         self.send_response(401)
         self.send_header('WWW-Authenticate', 'Basic realm="Demo Realm"')
         self.send_header("Cache-Control", "no-cache")
         self.send_header('Content-type','application/json')
         self.send_header('Access-Control-Allow-Origin', 'null')
         self.send_header('Access-Control-Allow-Credentials', 'true')
         self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
         self.send_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
         self.send_header("Access-Control-Allow-Headers", "Authorization")
         self.end_headers()

     def do_OPTIONS(self):
         self.send_response(200)
         self.send_header('Access-Control-Allow-Credentials', 'true')
         self.send_header('Access-Control-Allow-Origin', 'null')
         self.send_header('Access-Control-Allow-Methods', 'GET,OPTIONS')
         self.send_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
         self.send_header("Access-Control-Allow-Headers", "origin, Authorization, accept")
         self.send_header('Content-type','application/json')
         self.end_headers()




     def do_GET(self):
         global key

         if self.headers.get('Authorization') == None:
             self.do_AUTHHEAD()
             response = { 'success': False, 'error': 'No auth header received'}
             self.wfile.write(bytes(json.dumps(response), 'utf-8'))


         elif self.headers.get('Authorization') == 'Basic ' + str(key):
             resp=[]
             self.send_response(200)
             self.send_header('Allow', 'GET, OPTIONS')
             self.send_header("Cache-Control", "no-cache")
             self.send_header('Content-type','application/json')
             self.send_header('Access-Control-Allow-Origin', 'null')
             self.send_header('Access-Control-Allow-Credentials', 'true')
             self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
             self.send_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
             self.send_header("Access-Control-Allow-Headers", "Authorization")
             self.end_headers()
             req=str(self.path)[1:]
             if(req == "all" ):
                 try:
                     for i in range(0,units):
                         resp.append({varName[i]:[reg[i],varNameData[i]]})
                         i+=1
                     self.wfile.write(json.dumps( resp ).encode())

                 except Exception as e:
                     print('all',e)
             else:
                 for i in range(0,units):
                     if(req == varName[i] ):
                         try:
                             resp =json.dumps({ varName[i]:varNameData[i] }  )
                             self.wfile.write(resp.encode())
                         except Exception as e:
                             print(e)
                     i+=1
         else:
             self.do_AUTHHEAD()
             response = { 'success': False, 'error': 'Invalid credentials'}
             self.wfile.write(bytes(json.dumps(response), 'utf-8'))


     def do_POST(self):
             self.do_AUTHHEAD()
             response = { 'success': False, 'error': 'Invalid credentials'}
             self.wfile.write(bytes(json.dumps(response), 'utf-8'))

def set_auth( username, password):
         global key
         key = base64.b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

def run(server_class=HTTPServer, handler_class=S, port=8080):
     #logging.basicConfig(level=logging.INFO)

     server_address = (serverSlave, int(portSlave))
     httpd = server_class(server_address, handler_class)
     print('Starting httpd...\n')
     try:
         httpd.socket = ssl.wrap_socket (httpd.socket, certfile=pathFolder+'json_server.pem',ssl_version=ssl.PROTOCOL_TLSv1, server_side=True)
         httpd.serve_forever()
     except Exception as e:
         print(e)
         pass
     httpd.server_close()


def val_to_string(val):
     if isinstance(val, (list, tuple)):
         res = []
         for v in val:
             res.append(val_to_string(v))
         return "[" + ", ".join(res) + "]"

     if hasattr(val, "to_string"):
         val = val.to_string()
     elif isinstance(val, ua.StatusCode):
         val = val.name
     elif isinstance(val, (Enum, IntEnum)):
         val = val.name
     elif isinstance(val, ua.DataValue):
         val = variant_to_string(val.Value)
     elif isinstance(val, ua.XmlElement):
         val = val.Value
     elif isinstance(val, str):
         pass
     elif isinstance(val, bytes):
         val = val.decode("utf-8", errors="replace")
     elif isinstance(val, datetime):
         val = val.isoformat()
     elif isinstance(val, (int, float)):
         val = str(val)
     else:
         val = str(val)
     return val
def variant_to_string(var):
     return val_to_string(var.Value)

def getModbusData(i):
         if(reg[i]=='READ_INPUT_REGISTERS'):   c=cst.READ_INPUT_REGISTERS
         if(reg[i]=='READ_DISCRETE_INPUTS'):   c=cst.READ_DISCRETE_INPUTS
         if(reg[i]=='READ_COILS'):             c=cst.READ_COILS
         if(reg[i]=='READ_HOLDING_REGISTERS'): c=cst.READ_HOLDING_REGISTERS
         print('Start:', varName[i])
         while True:
             try:
                 varNameData[i]= master[i].execute(int(rtuAddress[i]), c, int(startAdr[i]), int(rangeAdr[i])  )
             except Exception as e:
                 varNameData[i]=None
                 master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                 master[i].set_timeout(2)
             time.sleep(float(mTimeOut[i]))
             gc.collect()

def clientOPCUA(h):
     r=''
     global host
     global port
     url="opc.tcp://"+host[h] +":"+ port[h] +"/server/"
     try:
         client = Client(url)
         client.connect()
         r = client.get_root_node()
     except Exception as e:
         r=''
         pass
     return r


def getOPCUAData(h):
         objChildrenName=[]
         unitsChild=[]
         objChild=[]
         dataValue=[]
         root=''
         try:
             root=clientOPCUA(h)
             obj = root.get_child(["0:Objects"])
             objChild= obj.get_children()
             i=0
             for i in range(0,len(objChild)):
                 unitsChild.append(i)
                 unitsChild[i]=objChild[i].get_children()
                 parName=val_to_string(objChild[i].get_browse_name())[2:]
                 for a in range(0, len( unitsChild[i] ) ):
                     valName=val_to_string(unitsChild[i][a].get_browse_name())[2:]
                     try:
                         valData=unitsChild[i][a].get_value()
                         data =unitsChild[i][a].get_data_value()
                         st=val_to_string(data.StatusCode)
                         ts= data.ServerTimestamp.isoformat()
                         tsc= data.SourceTimestamp.isoformat()
                     except Exception as e:
                         pass

                     a+=1
                 i+=1
         except Exception as e:
             print ('First connect Error -- ',e)
             pass

         while True:
                 time.sleep(float(mTimeOut[h]))
                 b=None
                 b=[]
                 try:
                         obj = root.get_child(["0:Objects"])
                         objChild= obj.get_children()
                         i=0
                         for i in range(0,len(objChild)):
                             if(i>0):
                                 parName=val_to_string(objChild[i].get_browse_name())[2:]
                                 a=0
                                 for a in range(0, len( unitsChild[i] ) ):
                                     valName=val_to_string(unitsChild[i][a].get_browse_name())[2:]
                                     try:
                                         valData=unitsChild[i][a].get_value()
                                         data =unitsChild[i][a].get_data_value()
                                         st=val_to_string(data.StatusCode)
                                         ts= data.ServerTimestamp.isoformat()
                                         tsc= data.SourceTimestamp.isoformat()
                                         b.append({'Name':parName,'Param':valName,valName:valData,'Status':st,'ts':ts,'tsc':tsc})
                                     except Exception as e:
                                         pass
                                         print(e)
                                     a+=1
                             i+=1
                         varNameData[h]=b
                 except Exception as e:
                         pass
                         print ('Try connect -- ',e)
                         b= {"Status": "Error"}
                         varNameData[h]=b
                         objChild=None
                         unitsChild=None
                         unitsChild=[]
                         objChild=[]
                         root=''
                         try:
                             root=clientOPCUA(h)
                             obj = root.get_child(["0:Objects"])
                             objChild= obj.get_children()
                             i=0
                             for i in range(0,len(objChild)):
                                 unitsChild.append(i)
                                 unitsChild[i]=objChild[i].get_children()
                                 parName=val_to_string(objChild[i].get_browse_name())[2:]
                                 for a in range(0, len( unitsChild[i] ) ):
                                     valName=val_to_string(unitsChild[i][a].get_browse_name())[2:]
                                     try:
                                         valData=unitsChild[i][a].get_value()
                                         data =unitsChild[i][a].get_data_value()
                                         st=val_to_string(data.StatusCode)
                                         ts= data.ServerTimestamp.isoformat()
                                         tsc= data.SourceTimestamp.isoformat()
                                     except Exception as e:
                                         pass
                         except Exception as e:
                             print ('error connect while ',e)
                             pass

if __name__ == "__main__":

     serverSlave=''
     portSlave=0
     reg=[]
     startAdr=[]
     rangeAdr=[]
     rtuAddress=[]
     host=[]
     master=[]
     port=[]
     units=0
     modbusUnits=0
     mTimeOut=[]
     varName=[]
     varNameData=[]
     typeServ=[]
     opcuaData=[]
     key=''
     login=''
     password=''
     try:

         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')
         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])
         #idServ=str('12')
         #connDb = sqlite3.connect('d:\scadapy\main\db\webDb.db')
         cursor = connDb.cursor()
         for row in cursor.execute('SELECT ip,port,timeout,login,password FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             timeOut=row[2]
             login=row[3]
             password=row[4]
         cursor.execute("select param,regadr,regcount,ip,port,var,t,type from  master where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)
         for i in range(0,len(dt)):
                         typeServ.append(i)
                         rtuAddress.append(i)
                         reg.append(i)
                         startAdr.append(i)
                         rangeAdr.append(i)
                         host.append(i)
                         master.append(i)
                         port.append(i)
                         varName.append(i)
                         mTimeOut.append(i)
                         varNameData.append(i)
                         opcuaData.append(i)
                         rtuAddress[i] =  1
                         reg[i]        =  dt[i][0]
                         startAdr[i]   =  dt[i][1]
                         rangeAdr[i]   =  dt[i][2]
                         host[i]       =  dt[i][3]
                         port[i]       =  dt[i][4]
                         varName[i]    =  dt[i][5]
                         mTimeOut[i]   =  dt[i][6]
                         typeServ[i]   =  dt[i][7]

                         try:
                             master[i] = modbus_tcp.TcpMaster(host=host[i], port=int(port[i]))
                             master[i].set_timeout(2)
                         except Exception as e:
                          #   pass
                             print(e)
                         i+=1
     except Exception as e:
         print (e)
     try:
         print( 'Starting web server...')
         set_auth(login,password)
         for i in range(0,units):
             if(typeServ[i]=='modbus_tcp'):
                 print('start')
                 modb = threading.Thread(target=getModbusData,args=(i,))
                 modb.daemon = True
                 modb.start()
             if(typeServ[i]=='opc_ua'):
                 opc=threading.Thread(target=getOPCUAData,args=(i,))
                 opc.daemon = True
                 opc.start()
         run()
     except Exception as e:

         print(e)




