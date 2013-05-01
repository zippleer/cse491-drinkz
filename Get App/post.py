import sys
import socket



def postRequest(args):

    address = args[1]
    port = args[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((address, int(port)))

    s.send('POST / HTTP/1.0\r\n\r\n')
    text = ""
    while 1:
        buf = s.recv(1000)
        if not buf:
            break
        text+=buf
    print text

    s.close()

if __name__ == '__main__':
    postRequest(sys.argv)
