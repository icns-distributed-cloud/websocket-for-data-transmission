import socket 
import numpy as np
import cv2
import time
from queue import Queue
from _thread import *

def webcam(queue):
	
	cap = cv2.VideoCapture(0)
	cap.set(3,640)
	cap.set(4,480)
	
	while True:
		ret, frame = cap.read()
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
		result, imgencode = cv2.imencode('.jpg', frame, encode_param)
		data = np.array(imgencode)
		stringData = data.tostring()

		queue.put(stringData)
			
		# cv2.imshow('image', frame)
		# if cv2.waitKey(1) & 0xFF == ord('q'):
			#break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	
	enclosure_queue = Queue()
	
	#HOST = '163.180.117.43'
	HOST = '210.114.91.98'
	PORT = 9999
	
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client_socket.connect((HOST, PORT))
	start_new_thread(webcam, (enclosure_queue,))	
	i =1
	while True:
		message = '1'
		client_socket.send(message.encode())
		client_socket.recv(1024)
		
		stringData = enclosure_queue.get()
		# inform server the size of sending data
		client_socket.send(str(len(stringData)).ljust(16).encode())
		# send data
		client_socket.send(stringData)
		print(i)
		i = i+1
	
	client_socket.close()
