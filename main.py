import pygame as pg
import socket
import json
data = {'player1' : {}}
me = None
windows = pg.display.set_mode((1000, 700), pg.DOUBLEBUF)
you = None
playe2 = None

class Player():
    def __init__(self, args):
        self.image = pg.transform.scale(pg.image.load(args[0]), (args[1], args[2]))
        self.rect = self.image.get_rect()
        self.speed = args[3]
        self.fir = False
        self.pulspeed = args[4]
        self.display=args[5]
        self.rect.x = args[6]
    def update(self):
        if pg.key.get_pressed()[pg.K_UP] and self.rect.top > 0 :
            self.rect.y -= self.speed
        if pg.key.get_pressed()[pg.K_DOWN]and self.rect.bottom < 700:
            self.rect.y += self.speed
        if pg.key.get_pressed()[pg.K_SPACE] and self.fir == False:
            self.fire()
        elif self.fir == True:
            if self.pulrect.x > 1000:
                self.pulrect = None
                self.pul = None
                self.fir = False
            else:
                self.pulrect.x += self.pulspeed
                self.display.blit(self.pul, self.pulrect)
        self.display.blit(self.image, self.rect)
    def manup(self):
        self.display.blit(self.image, self.rect)
    def fire(self):
        if self.fir == False:
            self.pul = pg.transform.scale((pg.image.load('pupilka.png')), (20, 20))
            self.pulrect = self.pul.get_rect()

            self.pulrect.x = self.rect.right
            self.pulrect.y = self.rect.y +50
            self.fir = True
#server transmit function
def connec(type):
    global data , me , you , playe2
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(300)
    #Get headers
    if type == 'GET':
        dat = {'headers' : 'GET' , 'room' : 1 , 'game' : {}}
        sock.connect(('192.168.1.188', 2222))
        sock.send(json.dumps(dat).encode('utf-8'))
        try:
            if me == 'player1':
                data['player2'] = json.loads(sock.recv(1048576).decode('utf-8'))['player2']
                playe2.rect.x = data['player2']['transform'][0]
                playe2.rect.y = data['player2']['transform'][1]
            if me == 'player2':
                data['player1'] = json.loads(sock.recv(1048576).decode('utf-8'))['player1']
                playe2.rect.x = data['player1']['transform'][0]
                playe2.rect.y = data['player1']['transform'][1]
        except:
            pass


    #Post headers
    if type == 'POST':
        dat = {'headers': 'POST' , 'room' : 1 , 'game' : data}
        sock.connect(('192.168.1.188' , 2222))
        sock.send(json.dumps(dat).encode('utf-8'))

    #Room connect headers
    if type == 'CONN':
        dat = {'headers' : 'CONN' , 'room' : 1 , 'game' : {}}
        sock.connect(('192.168.1.188' , 2222))
        sock.send(json.dumps(dat).encode('utf-8'))
        da = json.loads(sock.recv(1048576).decode('utf-8'))
        print(da['status'])
        if da['status'] == 'admin':
            me = 'player1'
            you = Player(['1.png', 150, 150, 5, 5, windows, 0])
            playe2 = Player(['1.png', 150, 150, 5, 5, windows, 840])
        elif da['status'] == 'connected':
            me = 'player2'
            you = Player(['1.png', 150, 150, 5, 5, windows, 840])
            playe2 = Player(['1.png', 150, 150, 5, 5, windows, 0])

#Parsing function
def parse():
    global data , me , you
    if me == 'player1':
        data['player1'] = {'transform' : [you.rect.x , you.rect.y]}
        if hasattr(you , 'pulrect'):
            try:
                data['player1']['pul'] = [you.pulrect.x , you.pulrect.y]
            except:
                data['player1']['pul'] = None

    if me == 'player2':
        data['player2'] = {'transform' : [you.rect.x , you.rect.y]}
        if hasattr(you , 'pulrect'):
            try:
                data['player2']['pul'] = [you.pulrect.x , you.pulrect.y]
            except:
                data['player2']['pul'] = None

try:
    connec('CONN')
except Exception as e:
    print(str(e))

tick = 0
game = True
bg = pg.transform.scale(pg.image.load('3.jpg'), (1000, 700))
clock = pg.time.Clock()
while game == True:

    windows.blit(bg, (0, 0))
    ev = pg.event.get()
    for e in ev:
        if e.type == pg.QUIT:
            game = False
    pg.display.set_caption(str(clock.get_fps()))
    if tick == 5:
        connec("GET")
        parse()
        connec("POST")
        tick = 0
    you.update()
    playe2.manup()
    pg.display.update()
    clock.tick(60)
    tick += 1
