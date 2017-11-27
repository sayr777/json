
import sys
import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import gc
import os
import socket
import struct
import select
import threading

import sqlite3


if sys.platform == "win32":
     # On Windows, the best timer is time.clock()
    # print(sys.platform)
     default_timer = time.clock
else:
     # On most other platforms the best timer is time.time()
     default_timer = time.time

 # From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.


def checksum(source_string):
     """
     I'm not too confident that this is right but testing seems
     to suggest that it gives the same answers as in_cksum in ping.c
     """
     sum = 0
     countTo = len(source_string)
     count = 0
     while count < countTo:
         thisVal = source_string[count +1] * 256 + source_string[count]
         sum = sum + thisVal
         sum = sum & 0xffffffff  # Necessary?
         count = count + 2

     if countTo < len(source_string):
         sum = sum + ord(source_string[len(source_string) - 1])
         sum = sum & 0xffffffff  # Necessary?

     sum = (sum >> 16) + (sum & 0xffff)
     sum = sum + (sum >> 16)
     answer = ~sum
     answer = answer & 0xffff

     # Swap bytes. Bugger me if I know why.
     answer = answer >> 8 | (answer << 8 & 0xff00)

     return answer


def receive_one_ping(my_socket, ID, timeout):
     """
     receive the ping from the socket.
     """
     timeLeft = timeout
     while True:
         startedSelect = default_timer()
         whatReady = select.select([my_socket], [], [], timeLeft)
         howLongInSelect = (default_timer() - startedSelect)
         if whatReady[0] == []:  # Timeout
             return

         timeReceived = default_timer()
         recPacket, addr = my_socket.recvfrom(1024)
         icmpHeader = recPacket[20:28]
         type, code, checksum, packetID, sequence = struct.unpack(
             "bbHHh", icmpHeader
         )
         # Filters out the echo request itself.
         # This can be tested by pinging 127.0.0.1
         # You'll see your own request
         if type != 8 and packetID == ID:
             bytesInDouble = struct.calcsize("d")
             timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
             return timeReceived - timeSent

         timeLeft = timeLeft - howLongInSelect
         if timeLeft <= 0:
             return


def send_one_ping(my_socket, dest_addr, ID):
     """
     Send one ping to the given >dest_addr<.
     """
     dest_addr = socket.gethostbyname(dest_addr)

     # Header is type (8), code (8), checksum (16), id (16), sequence (16)
     my_checksum = 0

     # Make a dummy heder with a 0 checksum.
     header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
     bytesInDouble = struct.calcsize("d")
     data = (192 - bytesInDouble) * "Q"
     data = struct.pack("d", default_timer())+ data.encode()

     # Calculate the checksum on the data and the dummy header.
     my_checksum = checksum(header + data)

     # Now that we have the right checksum, we put that in. It's just easier
     # to make up a new header than to stuff it into the dummy.
     header = struct.pack(
         "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
     )
     packet = header + data
     my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1


def do_one(dest_addr, timeout=4):
     """
     Returns either the delay (in seconds) or none on timeout.
     timeout default is same as Windows Cmd
     """
     icmp_protocol = socket.getprotobyname("icmp")
     my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_protocol)
     my_ID = threading.current_thread().ident & 0xFFFF
     send_one_ping(my_socket, dest_addr, my_ID)
     delay = receive_one_ping(my_socket, my_ID, timeout)

     my_socket.close()
     return delay


def verbose_ping(dest_addr, timeout=2, count=4):
     """
     Send >count< ping to >dest_addr< with the given >timeout< and display
     the result.
     """
     for i in range(count):
         print("ping '{}' ... ".format(dest_addr), end='')
         try:
             delay = do_one(dest_addr, timeout)
         except socket.gaierror as e:
             print("Failed. (socket error: '{}')".format(e[1]))
             break

         if delay is None:
             print("Timeout > {}s".format(timeout))
         else:
             delay = delay * 1000
             print("{}ms".format(int(delay)))
     print


if __name__ == "__main__":

     serverSlave=''
     portSlave=0
     host=[]
     namePoint=[]
     units=0
     pingData=0




     try:
         count=0
         pathFolder =os.path.abspath(sys.argv[0]).replace(os.path.basename(__file__),'')

         idServ=sys.argv[1]
         connDb = sqlite3.connect(sys.argv[2])
         cursor = connDb.cursor()

         cursor.execute("select ip,name from  master_ping where serverId = "+ idServ)
         dt=cursor.fetchall()
         units=len(dt)
           
         for i in range(0,len(dt)):
             host.append(i)
             host[i]=dt[i][0]
             namePoint.append(i)
             namePoint[i]=dt[i][1]
             i+=1
             
 

         for row in cursor.execute('SELECT ip,port,tty,speed,timeout FROM servers where id ='+idServ):
             serverSlave=row[0]
             portSlave=row[1]
             tty=row[2]
             ttySpeed=row[3]
             timeOut=row[4]                
        
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
         print ('Starting server...')

         while True:
             for i in range(0,units):
                     try:
                         ret = do_one(host[i], 2)
                         if(ret==None):
                             mes="Error"
                             pingData=0
                         else:
                             pingData=1
                             mes="_Ok_"

                         if(pingData == 1):
                             slave.set_values('1', i, 1)
                         else:
                             slave.set_values('1', i, 0)

                         print ( 'DISCRETE_INPUTS '+time.strftime('%d-%m-%Y %H:%M:%S'), host[i] , pingData,mes, namePoint[i])

                     except Exception as e:
                         slave.set_values('1', i, 0)

                     time.sleep(float(timeOut))
                      
             gc.collect()


     except modbus_tk.modbus.ModbusError as e:
        # logger.error("%s- Code=%d" % (e, e.get_exception_code()))
         print ('Error')





