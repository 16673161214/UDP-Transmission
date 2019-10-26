# -*- coding: UTF-8 -*-
import os
import struct
from tqdm import tqdm
from socket import *
DEST_IP = '127.0.0.1'
DEST_PORT = 12000
batch_size=1000
filename = r'C:\Users\Administrator\Documents\cse205 assignment1\中国大学MOOC（慕课）_3.14.1（正版）.ipa'
for i in range(len(filename)-1,0,-1):
    if filename[i]=='.':
        suffix=filename[i:]
        break
filesize = os.path.getsize(filename)
client = socket(AF_INET, SOCK_DGRAM)
print("send the filetype to the server.")
suf=struct.pack('4s',suffix.encode('utf-8'))
client.sendto(suf,(DEST_IP, DEST_PORT))
print("send the filesize to the server.")
size=struct.pack('i',filesize)
client.sendto(size, (DEST_IP, DEST_PORT))
print("send the batchsize to the server.")
batchsize=struct.pack('i',batch_size)
client.sendto(batchsize, (DEST_IP, DEST_PORT))
f = open(filename, "rb")
data = []
print('Firstly, unpack the file:')
for i in tqdm(range(0, filesize)):
    (ch,) = struct.unpack("B", f.read(1))
    data.append(ch)
print('Then, pack the file and send it:')
count=0
string=b''
for i in tqdm(range(0, filesize)):
    element = struct.pack("B", data[i])
    string=string+element
    count+=1
    if count==batch_size:
        client.sendto(string, (DEST_IP, DEST_PORT))
        respond=client.recv(1024)
        count=0
        string=b''
    if i==filesize-1:
        client.sendto(string, (DEST_IP, DEST_PORT))
        count=0
        string=b''
print('have sent')
client.close()