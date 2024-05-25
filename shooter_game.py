#Создай собственный Шутер!

from pygame import *
from random import randint

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))
lost = 0
kill = 0
finish = False

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

run = True
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

player = Player('rocket.png', 200, 400, 65, 65, 7)

font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 30)
font3 = font.SysFont('Arial', 30)

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(50):
    monster = Enemy('ufo.png', randint(80, win_width - 80), randint(0, 100), 80, 50, 4)
    monsters.add(monster)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background,(0, 0))
        if sprite.groupcollide(monsters, bullets, True, True):
            kill += 1
            monster = Enemy('ufo.png', randint(80, win_width-80), randint(0, 100), 80, 50, 2)
            monsters.add(monster)
        #if sprite.spritecollide(player, monsters, False):
           # text_win = font3.render('YOU PROIGRAL!', 1, (255, 0, 0))
            #window.blit(text_win, (250, 250))
            #finish = True
        if lost >= 999:
            text_win = font3.render('YOU PROIGRAL!', 1, (255, 0, 0))
            window.blit(text_win, (250, 250))
            finish = True
        if kill >= 1099:
            text_win = font3.render('YOU POBEDIL!', 1, (0, 255, 0))
            window.blit(text_win, (250, 250))
            finish = True

        text_s = font1.render('Счёт:' + str(kill), 1, (255, 255, 255))
        text_lose = font2.render('Пропушено:' + str(lost), 1, (255, 255, 255))
        
        window.blit(text_lose, (5, 5))
        window.blit(text_s, (5, 30))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        player.fire()
        bullets.draw(window)
        bullets.update()
        clock.tick(FPS)
    display.update()