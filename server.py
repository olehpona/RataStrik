import socket
import json
data = {}
#data structure {room : {'player1' : {} , 'player2' : {}} , ...}
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(('127.0.0.1' , 2222))
server.listen(5)

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
                packeg = {'status' : 'connected'}
            else:
                packeg = {'status': 'full'}
        else:
            data[room] = {}
            packeg = {'status' : 'admin'}
        return packeg

while True:
    c , addr = server.accept()
    print(data)
    resived = json.loads(c.recv(1048576).decode('utf-8'))
    retur = parser(resived)
    if (retur != 1):
        c.send(json.dumps(retur).encode('utf-8'))

    c.close()


