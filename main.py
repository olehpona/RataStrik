import pygame as pg

windows = pg.display.set_mode((1000, 700), pg.DOUBLEBUF)


class Player():
    def __init__(self, args):
        self.image = pg.transform.scale(pg.image.load(args[0]), (args[1], args[2]))
        self.rect = self.image.get_rect()
        self.speed = args[3]
        self.fir = False
        self.pulspeed = args[4]
        self.display=args[5]

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

    def fire(self):
        if self.fir == False:
            self.pul = pg.transform.scale((pg.image.load('pupilka.png')), (20, 20))
            self.pulrect = self.pul.get_rect()

            self.pulrect.x = self.rect.right
            self.pulrect.y = self.rect.y +50
            self.fir = True


game = True
bg = pg.transform.scale(pg.image.load('3.jpg'), (1000, 700))
clock = pg.time.Clock()
you = Player(['1.png', 150, 150, 5, 5 , windows])
while game == True:
    windows.blit(bg, (0, 0))
    ev = pg.event.get()
    for e in ev:
        if e.type == pg.QUIT:
            game = False
    pg.display.set_caption(str(clock.get_fps()))
    you.update()
    pg.display.update()
    clock.tick(60)
