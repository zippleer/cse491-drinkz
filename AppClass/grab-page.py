import socket, sys

if len(sys.argv) != 3:
    print "Please enter the hostname, space, then a port"
    exit(0)
    
hostname = sys.argv[1]
port = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname , int(port)))

#asking the server for the index page
s.send("GET / HTTP/1.0\r\n\r\n")

#grabs pieces until there is no more info to grab
while 1:
    buf = s.recv(100)
    if not buf:
        break 
    print buf
sys.stdout.flush()
s.close()
