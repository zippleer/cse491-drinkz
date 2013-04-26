#!/usr/bin/env python
import sys
import socket

s = socket.socket()
host = socket.gethostname()
port = int(sys.argv[1])                 # take the port in from cmd line

print 'connecting...'
s.connect((host, port))
s.send('GET / HTTP/1.0\r\n\r\n')

buffer = ""
while "\r\n\r\n" not in buffer:
    data = s.recv(1024)
    buffer += data
s.close()

print 'got buffer:', buffer
# parsing the results for HW 5.4 is left as an exercise for the reader.
# (see server.py for the basic logic.)
