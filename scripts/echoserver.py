#!/usr/bin/env python

import socket

"""
A simple echo server
"""

host = '127.0.0.1'
#host = '192.168.0.30'
port = 21012
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

print 'Echo running on %s:%d' % (host, port)
while True:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        #print data
        client.send(data)
    client.close()
