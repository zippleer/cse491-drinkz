#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr

   buffer = c.recv(1024)

   while "\r\n\r\n" not in buffer:
      data = c.recv(1024)
      if not data:
         break
      buffer += data
      print (buffer,)
      time.sleep(1)

   print 'got entire request:', (buffer,)

   c.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\nHello, world.")
   c.close()
