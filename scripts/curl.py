import os

# TODO read from sys.args
METHOD = 'POST'
FILE = 'test.json'
HOST = '127.0.0.1'
PORT = '21012'

os.execv('/usr/bin/curl', ['usr/bin/curl', '-H', 'Content-Type: application/json', '-X' ,
    METHOD, '-d', '@'+FILE, '%s:%s' % (HOST, PORT)])
