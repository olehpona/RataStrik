import pygame as pg
import socket
import json
room = 0
pg.init()
pg.mixer.init()
pg.mixer.music.load('resourse/audio/music/1.mp3')
pg.mixer.music.play(0)
gamemode = 0
windows = pg.display.set_mode((1000, 700), pg.DOUBLEBUF)
bg = pg.transform.scale(pg.image.load('resourse/textures/menu.jpg'), (1000, 700))
class Button():
    def __init__(self , text , pos , func , disp):
        self.text = text
        self.pos = pos
        self.func = func
        fond = pg.font.Font('freesansbold.ttf', 15)
        self.font = fond.render(text, True, (0 , 0 , 0))
        self.fontrect = self.font.get_rect()
        self.image = pg.transform.scale(pg.image.load('resourse/textures/button.png'), (200 , 200))
        self.rect = self.image.get_rect()
        self.disp = disp
        x , y = pos
        self.rect.x = x
        self.rect.y = y
        x , y = self.rect.center
        self.fontrect.x = x
        self.fontrect.y = y
    def update(self , event):
        x, y = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.func()
    def render(self):
        self.disp.blit(self.image , self.rect)
        self.disp.blit(self.font, self.fontrect)
def play():
    global gamemode
    gamemode = 1
def quitf():
    quit()
play = Button('PLAY' ,  (50 , 50) , play , windows)
quuit = Button('QUIT' ,  (50 , 400) , quitf , windows)












data = {'player1' : {}}
me = None

you = None
playe2 = None

font = pg.font.Font('freesansbold.ttf', 32)
ip = '127.0.0.1'
# create a text surface object,
# on which text is drawn on it.
lose = font.render('LOSE', True, (200 , 0 , 0))
win = font.render('win', True, (200 , 0 , 0))
ent = font.render('ENTER ROOM ID AND PRESS SPACE' , True , (0 , 0 , 0))
# create a rectangular object for the
# text surface object
loseRect = lose.get_rect()
winRect = win.get_rect()
entRect = ent.get_rect()
# set the center of the rectangular object.
loseRect.center = (1000 // 2, 700 // 2)
winRect.center = (1000 // 2, 700 // 2)
class Player():
    def __init__(self, args):
        self.image = pg.transform.scale(pg.image.load(args[0]), (args[1], args[2]))
        self.rect = self.image.get_rect()
        self.speed = args[3]
        self.fir = False
        self.pulspeed = args[4]
        self.display=args[5]
        self.rect.x = args[6]
        self.me = args[7]
        self.status = 'Ok'
    def update(self):
        if pg.key.get_pressed()[pg.K_UP] and self.rect.top > 0 :
            self.rect.y -= self.speed
        if pg.key.get_pressed()[pg.K_DOWN]and self.rect.bottom < 700:
            self.rect.y += self.speed
        if pg.key.get_pressed()[pg.K_SPACE] and self.fir == False:
            self.fire()
        elif self.fir == True:
            if self.me == 'player1':
                if self.pulrect.x > 1000:
                    self.pulrect = None
                    self.pul = None
                    self.fir = False
                else:
                    self.pulrect.x += self.pulspeed
                    self.display.blit(self.pul, self.pulrect)
            else:
                if self.pulrect.x < 0:
                    self.pulrect = None
                    self.pul = None
                    self.fir = False
                else:
                    self.pulrect.x -= self.pulspeed
                    self.display.blit(self.pul, self.pulrect)
        self.display.blit(self.image, self.rect)
    def manup(self):
        self.display.blit(self.image, self.rect)
        try:
            self.display.blit(self.pul, self.pulrect)
        except:
            pass
    def fire(self):
        if self.fir == False:
            self.pul = pg.transform.scale((pg.image.load('resourse/textures/pupilka.png')), (20, 20))
            self.pulrect = self.pul.get_rect()

            self.pulrect.x = self.rect.right
            self.pulrect.y = self.rect.y +50
            self.fir = True
#server transmit function
def connec(type):
    global data , me , you , playe2 , ip , room
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3000)
    #Get headers
    if type == 'GET':
        dat = {'headers' : 'GET' , 'room' : room , 'game' : {}}
        sock.connect((ip, 2222))
        sock.send(json.dumps(dat).encode('utf-8'))
        try:
            if me == 'player1':
                data['player2'] = json.loads(sock.recv(1048576).decode('utf-8'))['player2']
                playe2.rect.x = data['player2']['transform'][0]
                playe2.rect.y = data['player2']['transform'][1]
                playe2.status = data['player2']['status']
                if 'pul' in data['player2'].keys():
                    if data['player2']['pul'] != None:
                        if not hasattr(playe2 , 'pulrect') or playe2.pulrect == None:
                            playe2.fire()
                        playe2.pulrect.x = data['player2']['pul'][0]
                        playe2.pulrect.y = data['player2']['pul'][1]
                    else:
                        playe2.pulrect = None

            if me == 'player2':
                data['player1'] = json.loads(sock.recv(1048576).decode('utf-8'))['player1']
                playe2.rect.x = data['player1']['transform'][0]
                playe2.rect.y = data['player1']['transform'][1]
                playe2.status = data['player1']['status']
                if 'pul' in data['player1'].keys():
                    if data['player1']['pul'] != None:
                        if not hasattr(playe2 , 'pulrect') or playe2.pulrect == None:
                            playe2.fire()
                        playe2.pulrect.x = data['player1']['pul'][0]
                        playe2.pulrect.y = data['player1']['pul'][1]
                    else:
                        playe2.pulrect = None
        except:
            pass


    #Post headers
    try:
        if type == 'POST':
            dat = {'headers': 'POST' , 'room' : room , 'game' : { 'me' : me , 'data': data[me]}}
            sock.connect((ip , 2222))
            sock.send(json.dumps(dat).encode('utf-8'))
    except Exception as h:
        print(str(h))
    #Room connect headers
    if type == 'CONN':
        dat = {'headers' : 'CONN' , 'room' : room , 'game' : {}}
        sock.connect((ip , 2222))
        sock.send(json.dumps(dat).encode('utf-8'))
        da = json.loads(sock.recv(1048576).decode('utf-8'))
        if da['status'] == 'admin':
            me = 'player1'
            you = Player(['1.png', 150, 150, 5, 5, windows, 0 , me])
            playe2 = Player(['1.png', 150, 150, 5, 5, windows, 840 , me])
        elif da['status'] == 'connected':
            me = 'player2'
            you = Player(['1.png', 150, 150, 5, 5, windows, 840,me])
            playe2 = Player(['1.png', 150, 150, 5, 5, windows, 0,me])
    if type == 'DISCONN':
        dat = {'headers' : 'DISCONN' , 'room' : room , 'game' : {'me': me}}
        print(dat)
        sock.send(json.dumps(dat).encode('utf-8'))
#Parsing function
def parse():
    global data , me , you , playe2
    try:
        if me == 'player1':
            data['player1'] = {'status' : you.status , 'transform' : [you.rect.x , you.rect.y]}
            if hasattr(you , 'pulrect')or you.pulrect != None:
                try:
                    data['player1']['pul'] = [you.pulrect.x , you.pulrect.y]
                except:
                    data['player1']['pul'] = None

        if me == 'player2':
            data['player2'] = {'status' : you.status ,'transform' : [you.rect.x , you.rect.y]}
            if hasattr(you , 'pulrect') or you.pulrect != None:
                try:
                    data['player2']['pul'] = [you.pulrect.x , you.pulrect.y]
                except:
                    data['player2']['pul'] = None
    except:
        pass


room = ''
stat = 0
tick = 0
game = True
clock = pg.time.Clock()
while game == True:
    windows.blit(bg, (0, 0))
    if gamemode == 0:
        play.render()
        quuit.render()
        ev = pg.event.get()
        for e in ev:
            play.update(e)
            quuit.update(e)
            if e.type == pg.QUIT:
                game = False
    if gamemode == 1:
        windows.blit(ent , entRect)
        ev = pg.event.get()
        for e in ev:
            if e.type == pg.QUIT:
                game = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    gamemode = 2
                    room = int(room)
                    connec('CONN')
                if e.key == pg.K_0:
                    room += '0'
                if e.key == pg.K_1:
                    room += '1'
                if e.key == pg.K_2:
                    room += '2'
                if e.key == pg.K_3:
                    room += '3'
                if e.key == pg.K_4:
                    room += '4'
                if e.key == pg.K_5:
                    room += '5'
                if e.key == pg.K_6:
                    room += '6'
                if e.key == pg.K_7:
                    room += '7'
                if e.key == pg.K_8:
                    room += '8'
                if e.key == pg.K_9:
                    room += '9'


    if gamemode == 2:
        ev = pg.event.get()
        for e in ev:
            if e.type == pg.QUIT:
                game = False
        pg.display.set_caption(str(clock.get_fps()))
        connec("GET")
        parse()
        connec("POST")
        try:
            if pg.Rect.colliderect(you.rect , playe2.pulrect) or stat == 1:
                you.status = 'lose'
                windows.blit(lose, loseRect)
                stat = 1
            if playe2.status == 'lose' or stat == 2:
                windows.blit(win , winRect)
                stat = 2
        except:
            pass

        you.update()
        playe2.manup()
    pg.display.update()
    clock.tick(60)
    tick += 1
