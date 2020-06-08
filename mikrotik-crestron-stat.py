from pysnmp.hlapi import *
import socket
import sys
import datetime
from time import sleep

crestron_ip = '192.168.0.5'
crestron_port = 505

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (crestron_ip, crestron_port)

while 1:
  current_time1 = datetime.datetime.now()
  errorIndication, errorStatus, errorIndex, varBinds = next(
       getCmd(SnmpEngine(),
          CommunityData('rb1100'),
          UdpTransportTarget(('192.168.0.19', 161)),
          ContextData(),
          ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.10.3')),
          ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.6.3')),
          ObjectType(ObjectIdentity('1.3.6.1.2.1.4.24.4.1.16.0.0.0.0.0.0.0.0.0.10.1.1.1'))
          )
  )

  bytesIn_check1 =  varBinds[0][1]
  bytesOut_check1 = varBinds[1][1]
  active_route_intelcom = int(varBinds[2][1])
  sleep(1)

  errorIndication, errorStatus, errorIndex, varBinds = next(
       getCmd(SnmpEngine(),
          CommunityData('rb1100'),
          UdpTransportTarget(('192.168.0.19', 161)),
          ContextData(),
          ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.10.3')),
          ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.6.3'))          
          )
  )

  time_delta = datetime.datetime.now() - current_time1
  micross = float(time_delta.microseconds + time_delta.seconds*1000000) / 1000000
  #print "Time difference in microseconds is: %0.2f" % micross

  bytesIn_check2 =  varBinds[0][1]
  bytesOut_check2 = varBinds[1][1]  

  RX_loading = ((float(bytesIn_check2-bytesIn_check1))*8/1048576) / micross
  TX_loading = ((float(bytesOut_check2-bytesOut_check1))*8/1048576) / micross

  if active_route_intelcom:
    sent = sock.sendto("|Intelcom|" + str(format(RX_loading,'.2f')) + "Mbps / " + str(format(TX_loading,'.2f')) + " Mbps|", server_address)
  else:
    sent = sock.sendto("|Megafon|" + str(format(RX_loading,'.2f')) + "Mbps / " + str(format(TX_loading,'.2f')) + " Mbps|", server_address)  


sock.close()

