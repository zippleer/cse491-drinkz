import socket, sys, os

if len(sys.argv) != 3:
    print "Please enter the hostname, space, then a port"
    exit(0)
 
def test_GET():
    hostname = sys.argv[1]
    port = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname , int(port)))

    #asking the server for the index page
    s.send("GET / HTTP/1.0\r\n\r\n")
    
    reply = "" 
    #grabs pieces until there is no more info to grab
    while 1:
        buf = s.recv(100)
        if not buf:
            break 
        reply += buf

    assert reply.find("Hi there! This is my app"), t
    print "GET test: pass"
    sys.stdout.flush()
    s.close()

def test_Form():
    hostname = sys.argv[1]
    port = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname , int(port)))

    #asking the server for the index page
    s.send("GET /recv?in=good HTTP/1.0\r\n\r\n")

    reply = "" 
    #grabs pieces until there is no more info to grab
    while 1:
        buf = s.recv(100)
        if not buf:
           break 
        reply += buf

    assert reply.find('good')
    assert reply.find('form')
    sys.stdout.flush()
    print "Form test: pass"
    s.close()

def test_PIC():
    hostname = sys.argv[1]
    port = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname , int(port)))

    #asking the server for the index page
    s.send("GET /pic HTTP/1.0\r\n\r\n")
    
    reply = '' 
    buf = ''
    #grabs pieces until there is no more info to grab
    while 1:
        buf = s.recv(100)
        if not buf:
           break 
        if '\r\n' in buf:
            continue
        else:
            reply += buf
        
    pic = open('Spartan-hemlet-Black-150-pxls.gif','wb')
    pic.write(reply)
    size = pic.tell()
    
    assert os.path.exists('Spartan-hemlet-Black-150-pxls.gif')

    pic.close()

    #Test see if a file exsists and how many bytes does it have
    sys.stdout.flush()
    print "Image retrieval: pass"
    s.close()


if __name__ == "__main__":
    test_GET()
    test_PIC()
    test_Form()
