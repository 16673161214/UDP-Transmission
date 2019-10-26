# -*- coding: UTF-8 -*-
import struct
from socket import *
from tqdm import tqdm
DEST_IP = '127.0.0.1'
DEST_PORT = 12000
server = socket(AF_INET, SOCK_DGRAM)  # define socket type
server.bind(('', DEST_PORT))  # bind the listening IP and Port, a tuple format
print('Server is ready to receive.')
suffix = server.recv(1024)
suf = suffix.decode()
print('filetype is ' + suf)
filesize = server.recv(1024)
filesize = struct.unpack('i', filesize)
fsize = filesize[0]
print('filesize is ' + str(fsize))
batchsize = server.recv(1024)
batchsize = struct.unpack('i', batchsize)
bsize = batchsize[0]
print('batchsize is ' + str(bsize))
file = b''
num=fsize/bsize
if num%1!=0:
    num=int(num)+1
else:
    num=int(num)
try:
    with tqdm(total=fsize) as bar:
        for i in range(num-1):
            data, address = server.recvfrom(34000)  # receive data from client-side
            file = file + data
            server.sendto('ok'.encode('utf-8'), address)
            bar.update(bsize)
        data, address = server.recvfrom(34000)  # receive data from client-side
        file = file + data
        bar.update(fsize-(num-1)*bsize)
    print('Connected by ', address)
except socket.error:
    print('error:', socket.error)
with open(r'C:\Users\Administrator\Documents\cse205 assignment1\receive' + suf, 'wb') as rec:
    rec.write(file)
    rec.close()
server.close()