FROM icnslab/project_gom:raspbian_opencv

MAINTAINER Seungjun "hongsj1022@khu.ac.kr"

RUN pip3 install --upgrade pip; pip3 install numpy
RUN apt-get -y update
RUN apt-get install -y --fix-missing git

WORKDIR /home/
RUN git clone https://github.com/icns-distributed-cloud/websocket-for-data-transmission.git
CMD python3 /home/image/client.py
