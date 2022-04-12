import socket
import json
from _thread import *
data = {}
#data structure {room : {'player1' : {} , 'player2' : {}} , ...}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2222))
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
        data[room][game['me']] = game['data']
        return 1
    elif reqv == 'CONN':
        if room in data.keys():
            if 'player2' in data[room]:
                if 'player1' in data[room]:
                    packeg = {'status': 'full'}
                else:
                    packeg = {'status': 'admin'}
            else:
                packeg = {'status' : 'connected'}
        else:
            data[room] = {}
            packeg = {'status' : 'admin'}
        print(packeg)
        return packeg
    elif reqv == 'DISCONN':
        print(game['me'])
        data[room].pop(game['me'])
        return 1
def client(c):
    resived = json.loads(c.recv(1048576).decode('utf-8'))
    retur = parser(resived)
    if (retur != 1):
        c.sendall(json.dumps(retur).encode('utf-8'))
    c.close()

while True:
    try:
        c , addr = server.accept()

        start_new_thread(client, (c , ))
        Thrid += 1
        print(data)
    except Exception as ex:
        print(str(ex))



