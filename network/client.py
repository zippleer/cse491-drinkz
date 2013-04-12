#!/usr/bin/env python
import sys
import socket

import drinkz.app

s = socket.socket()
host = socket.gethostname()
port = int(sys.argv[1])                 # take the port in from cmd line

print 'connecting...'
s.connect((host, port))
print 'got:'
print s.recv(1024)
print 'and next:'
print s.recv(1024)
s.send('DIEEIEDIEIE')
print 'done.'
s.close()
