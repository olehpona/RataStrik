import socket
import json
from _thread import *
data = {}
#data structure {room : {'player1' : {} , 'player2' : {}} , ...}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.188', 2222))
server.listen(15)
Thrid = 0
def parser(recv):
    global data
    reqv = recv['headers']
    game = recv['game']
    room = recv['room']
    if reqv == 'GET':
        packeg = data[room]
        return packeg
    elif reqv == 'POST':
        data[room] = game
        return 1
    elif reqv == 'CONN':
        if room in data.keys():
            if 'player2' in data[room]:
                packeg = {'status': 'full'}
            else:
                packeg = {'status' : 'connected'}
        else:
            data[room] = {}
            packeg = {'status' : 'admin'}
        return packeg
def client(c):
    resived = json.loads(c.recv(1048576).decode('utf-8'))
    retur = parser(resived)
    if (retur != 1):
        c.sendall(json.dumps(retur).encode('utf-8'))
    print(addr)
    c.close()

while True:

    c , addr = server.accept()

    start_new_thread(client, (c , ))
    Thrid += 1



