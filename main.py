import pygame as pg
import socket
import json
room = 0
with open('resourse/characters.json' , 'r') as file:
    charecters = json.load(file)


pg.init()

pg.mixer.init()

pg.mixer.music.load('resourse/audio/music/1.mp3')

pg.mixer.music.play(0)

fonts = pg.font.Font('freesansbold.ttf', 30)

gamemode = 0

settmode = 0

windows = pg.display.set_mode((1000, 700), pg.DOUBLEBUF)

bg = pg.transform.scale(pg.image.load('resourse/textures/menu.jpg'), (1000, 700))

character = ''

class Button():
    def __init__(self ,img,text , pos , func ,size , disp):
        self.text = text
        self.pos = pos
        self.func = func
        self.img = img
        fond = pg.font.Font('freesansbold.ttf', 15)
        self.font = fond.render(text, True, (0 , 0 , 0))
        self.fontrect = self.font.get_rect()
        self.image = pg.transform.scale(pg.image.load('resourse/textures/'+img), (size[0] , size[1]))
        self.rect = self.image.get_rect()
        self.disp = disp
        x , y = pos
        self.rect.x = x
        self.rect.y = y
        x , y = self.rect.center
        self.fontrect.x = x
        self.fontrect.y = y


    def update(self , event , compens):
        x, y = pg.mouse.get_pos()
        x -= compens[0]
        y -= compens[1]
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    print('abeme')
                    self.func(self.img)


    def render(self):
        self.disp.blit(self.image , self.rect)
        self.disp.blit(self.font, self.fontrect)


def play(temp):
    global gamemode
    gamemode = 1


def quitf(temp):
    quit()


def sett(temp):
    global settmode
    settmode = 1

def char(temp):
    global gamemode , character, chartext , charecters
    character = temp
    chartext = charecters[character]['text']


play = Button('button.png','PLAY' ,  (50 , 10) , play ,[200 , 200], windows)
quuit = Button('button.png','QUIT' ,  (50 , 400) , quitf ,[200 , 200], windows)
settin = Button('button.png','Setting' , (50 , 200) , sett , [200 , 200] , windows)


class Setting():
    def __init__(self , width = 300 , height = 500  , font = None , pos = [] ):
        self.size = (width , height)
        self.surface = pg.Surface(self.size)

        self.picture = pg.transform.scale(pg.image.load('resourse/textures/sett.png'),(width , height))
        self.valume = '100'
        self.pos = pos
        self.volumetext = font.render(self.valume , True , (0 , 0 ,0))
        self.volumerect = self.volumetext.get_rect()
        self.volumerect.x = 200
        self.volumerect.y = 150
        self.minus = Button('button.png',"-" , (25 , 50) , self.minu , [100 , 100] , self.surface)
        self.plus = Button('button.png',"+", (25, 150), self.plu, [100, 100], self.surface)


    def minu(self , temp):
        if int(self.valume) > 0:
            self.valume = str(int(self.valume) - 5)

    def plu(self, temp):
        if int(self.valume) < 100:
            self.valume =str(int(self.valume) + 5)


    def update(self , e , mixer):
        #ВОТ ТУТ НЕ РОБИТЬ
        self.surface.fill((8,   255, 0))
        mixer.music.set_volume(float(self.valume)/100)
        self.minus.render()
        self.plus.render()
        self.surface.blit(self.volumetext , self.volumerect)
        self.plus.update(e , self.pos)
        self.minus.update(e , self.pos)
        self.volumetext = font.render(self.valume, True, (0, 0, 0))




setting = Setting(font = fonts , pos = [350 , 80])










data = {'player1' : {}}
me = None

you = None
playe2 = None
chartext = '?'
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
        self.args = args
        self.image = pg.transform.scale(pg.image.load('resourse/textures/'+args[0]), (args[1], args[2]))
        self.rect = self.image.get_rect()
        self.speed = 0
        self.fir = False
        self.pulspeed = args[3]
        self.display=args[4]
        self.rect.x = args[5]
        self.me = args[6]
        self.character = args[0]
        self.atc = 0
        self.heath = 0
        self.status = 'Ok'
        self.hpstat = 0

    def init_self(self):
        global charecters
        if self.heath == charecters[self.character]['hp']:
            self.heath = charecters[self.character]['hp']
        if self.hpstat ==0:
            self.heath = charecters[self.character]['hp']
            self.hpstat =1
        self.atc = charecters[self.character]['atk']
        self.speed = charecters[self.character]['speed']
        try:
            self.image = pg.transform.scale(pg.image.load('resourse/textures/'+self.character), (self.args[1], self.args[2]))
        except:
            self.image = pg.transform.scale(pg.image.load('resourse/textures/' + '1.png'),(self.args[1], self.args[2]))


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
    def colision(self):
        self.pulrect = None
        self.pul = None
        self.fir = False
#client transmit function
def connec(type):
    global data , me , you , playe2 , ip , room , character
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
                playe2.character = data['player2']['character']
                playe2.init_self()
                if 'pul' in data['player2'].keys():
                    if data['player2']['pul'] != None:
                        if not hasattr(playe2 , 'pulrect') or playe2.pulrect == None:
                            playe2.fire()
                        playe2.pulrect.x = data['player2']['pul'][0]
                        playe2.pulrect.y = data['player2']['pul'][1]
                    else:
                        playe2.colision()

            if me == 'player2':
                data['player1'] = json.loads(sock.recv(1048576).decode('utf-8'))['player1']
                playe2.rect.x = data['player1']['transform'][0]
                playe2.rect.y = data['player1']['transform'][1]
                playe2.status = data['player1']['status']
                playe2.character = data['player1']['character']
                playe2.init_self()
                if 'pul' in data['player1'].keys():
                    if data['player1']['pul'] != None:
                        if not hasattr(playe2 , 'pulrect') or playe2.pulrect == None:
                            playe2.fire()
                        playe2.pulrect.x = data['player1']['pul'][0]
                        playe2.pulrect.y = data['player1']['pul'][1]
                    else:
                        playe2.colision()
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
            you = Player([character, 150, 150, 5, windows, 0 , me])
            playe2 = Player(['1.png', 150, 150, 5, windows, 840 , me])
        elif da['status'] == 'connected':
            me = 'player2'
            you = Player([character, 150, 150, 5, windows, 840,me])
            playe2 = Player(['1.png', 150, 150, 5, windows, 0,me])
    if type == 'DISCONN':
        dat = {'headers' : 'DISCONN' , 'room' : room , 'game' : {'me': me}}
        print(dat)
        sock.send(json.dumps(dat).encode('utf-8'))
    you.init_self()
#Parsing function
def parse():
    global data , me , you , playe2
    try:
        if me == 'player1':
            data['player1'] = {'status' : you.status , 'character' : you.character,  'transform' : [you.rect.x , you.rect.y]}
            if hasattr(you , 'pulrect')or you.pulrect != None:
                try:
                    data['player1']['pul'] = [you.pulrect.x , you.pulrect.y]
                except:
                    data['player1']['pul'] = None

        if me == 'player2':
            data['player2'] = {'status' : you.status ,'character' : you.character,'transform' : [you.rect.x , you.rect.y]}
            if hasattr(you , 'pulrect') or you.pulrect != None:
                try:
                    data['player2']['pul'] = [you.pulrect.x , you.pulrect.y]
                except:
                    data['player2']['pul'] = None
    except:
        pass

first =  Button('1.png','' , (50 , 50) , char , [150 , 150] , windows)
second = Button('2.png', '', (250, 50), char, [150, 150], windows)
third = Button('3.png', '', (400, 50), char, [150, 150], windows)
room = ''
stat = 0
tick = 0
game = True
clock = pg.time.Clock()

fonts = pg.font.Font('freesansbold.ttf', 25)

while game == True:
    windows.blit(bg, (0, 0))
    if gamemode == 0:
        play.render()
        quuit.render()
        settin.render()
        ev = pg.event.get()
        if settmode == 1:
            windows.blit(setting.surface , (350 , 80))
            if pg.key.get_pressed()[pg.K_ESCAPE]:
                settmode = 0

        for e in ev:
            play.update(e , [0 , 0])
            quuit.update(e, [0 , 0])
            settin.update(e, [0,0])
            setting.update(e , pg.mixer)
            if e.type == pg.QUIT:
                game = False
    if gamemode == 1:
        about = fonts.render(chartext , True , (0 , 100 , 0))
        abrect = about.get_rect()
        abrect.y = 600
        windows.blit(about , abrect)
        if pg.key.get_pressed()[pg.K_SPACE]:
            gamemode = 2
        first.render()
        second.render()
        third.render()
        ev = pg.event.get()
        for e in ev:
            first.update(e , [0 , 0])
            second.update(e, [0 , 0])
            third.update(e, [0,0])
            if e.type == pg.QUIT:
                game = False
    if gamemode == 2:
        windows.blit(ent , entRect)
        ev = pg.event.get()
        for e in ev:
            if e.type == pg.QUIT:
                game = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    gamemode = 3
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


    if gamemode == 3:
        ev = pg.event.get()
        for e in ev:
            if e.type == pg.QUIT:
                game = False
        pg.display.set_caption(str(clock.get_fps()))
        connec("GET")
        parse()
        connec("POST")
        try:
            if pg.Rect.colliderect(you.rect , playe2.pulrect):
                you.heath = you.heath - playe2.atc
                print(you.heath)
                if you.heath <= 0:
                    stat = 1
                    you.status = 'lose'
                    windows.blit(lose, loseRect)
                playe2.colision()

        except:
            pass
        if playe2.status == 'lose':
            windows.blit(win , winRect)
            stat = 2
        try:
            if pg.Rect.colliderect(playe2.rect , you.pulrect):
                you.colision()
        except:
            pass
        if stat == 1:
            windows.blit(lose, loseRect)
        if stat == 2:
            windows.blit(win, winRect)
        hp = fonts.render(str(you.heath) , True , (0 , 100 , 0))
        hprect = hp.get_rect()
        windows.blit(hp , hprect)
        if stat ==0:
            you.update()
            playe2.manup()
    pg.display.update()
    clock.tick(60)
    tick += 1
