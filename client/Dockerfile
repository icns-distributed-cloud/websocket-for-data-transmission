FROM icnslab/project_gom:raspbian_opencv

MAINTAINER Seungjun "hongsj1022@khu.ac.kr"

RUN pip3 install --upgrade pip; pip3 install numpy
RUN apt-get -y update
RUN mkdir /home/image

ADD ./ /home/image
CMD python3 /home/image/client.py
