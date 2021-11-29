import socket 
import numpy as np
import cv2
from queue import Queue
from _thread import *

enclosure_queue = Queue()


def webcam(queue):
    capture = cv2.VideoCapture(0)  #0번 카메라를 VideoCapture 타입의 객체로 받아옴

    while True:
        ret, frame = capture.read()

        if ret == False:
            continue


        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] #이미지 품질 90 0~100까지 설정해줄 수 있다.
        result, imgencode = cv2.imencode('.jpg', frame, encode_param) 

        data = np.array(imgencode)
        stringData = data.tostring()

        queue.put(stringData)

        
        cv2.imshow('image', frame)
            
        key = cv2.waitKey(1)
        if key == 27:
            break


HOST = '127.0.0.1'             #호스트는 16x.xxx.xxx.xx 학교 서버 주소
PORT = 9999

# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다. 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 

start_new_thread(webcam, (enclosure_queue,)) # parameter설명 : 
                                             # start_new_thread(target= 실제로 스레드가 실행할 함수, args=(그 함수에게 전달할 인자))
                                             # 근데 인자가 하나일 경우, (var) 식으로 괄호로 감싸기만 하면 파이썬 인터프리터는 이를 튜플이 아니라
                                             # 그냥 var로 인식함. 그러므로 인자가 하나라면 (var,) 식으로 입력해야만 튜플로 인식한다.
                                             # 스레드는 프로세스가 종료되면 자동으로 종료됨.

while True: 

    message = '1'
    client_socket.send(message.encode()) #encode : 문자열을 byte로 변환해줌 

    client_socket.recv(1024) #2 받아줌

    stringData = enclosure_queue.get()
    client_socket.send(str(len(stringData)).ljust(16).encode()) # 데이터 수신 확인. recv함수는 수신될 데이터의 크기를 미리 알아야 하기 때문에 서버에서 전송할 이미지의 크기를 보내서
    client_socket.send(stringData)                              # 클라이언트에서 수신받을 준비를 하게 하고 이미지를 전송한다.


client_socket.close() 