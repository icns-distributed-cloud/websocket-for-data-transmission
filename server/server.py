import socket 
import cv2
import numpy
from select import *
from _thread import *

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def threaded(client_socket, addr): 

    print('Connected by :', addr[0], ':', addr[1]) # addr[0] 클라이언트 주소, addr[1] 접속한 클라이언트 포트

    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    n = 0
    while True: 

        try:
           
            data = client_socket.recv(1024)        #client로 부터 1을 받음

            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])   
                break

            message = '2'
            client_socket.send(message.encode())   #수신확인 2전송 보내고 받고니까 이 과정 넣어야 할거 같아서 넣었는데 필요 없을 수도 있음
            
            #recv는 받을 때 까지 대기   즉 보내고 받고 보내고 받고 한번씩 일어나야됨. 1을 주고 이미지를 받고 1을 주고 이미지를 받고
            #근데 스레드를 사용하면 순서 상관없이 동시적으로 할 수 있음
            # 스레드는 프로세스 내부에서 병렬 처리를 하기 위해, 프로세스의 소스코드 내부에서 특정 함수만 따로 뽑아내어 분신을 생성하는 것임.
            # 즉 원래라면 하나의 절차를 따르며 해야하는 일들도, 스레드를 생성해서 돌릴 경우엔 동시 다발적으로 일을 할 수 있음.
            length = recvall(client_socket,16)
            
            stringData = recvall(client_socket, int(length))
            data = numpy.frombuffer(stringData, dtype="uint8")

            decimg = cv2.imdecode(data,1)
            cv2.imshow('Image', decimg)
            if n <10:
                cv2.imwrite('images/'+str(n)+'.jpg',decimg)
                n += 1

            key = cv2.waitKey(1)
            if key == 27:                #esc누르면 종료
                break



        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0],':',addr[1])
            break
             
    client_socket.close() 


HOST = '127.0.0.1'
PORT = 9999

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다. 

# 포트 사용중이라 연결할 수 없다는 
# WinError 10048 에러 해결를 위해 필요합니다. 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다. 
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
server_socket.bind(('', PORT)) 

# 서버가 클라이언트의 접속을 허용하도록 합니다.
server_socket.listen() 

print('server start')
socketList = [server_socket]

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다
while True: 

    print('wait')

    try:
        read_socket, write_socket, error_socket = select(socketList, [], [], 1)
    
        for sock in read_socket:
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                start_new_thread(threaded, (client_socket, addr,))
    except KeyboardInterrupt:
        break

server_socket.close() 