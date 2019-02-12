import pygame
from pygame.locals import *
from ship import *
from bullet import *
from alien import *
from random import *

#Game settings
pygame.init()
red = (255, 0, 0)
clock = pygame.time.Clock()
width = 480
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaga")
font = pygame.font.SysFont("Comic Sans MS", 40)
font1 = pygame.font.SysFont("Comic Sans MS", 30)
font2 = pygame.font.SysFont("Comic Sans MS", 20)

#image loading
image = pygame.image.load("galaga_back.png")
s = pygame.image.load("galaga_ship.png")
s_temp = pygame.image.load("galaga_ship_temp.png")
bullet1 = pygame.image.load("galaga_bullet.png")
bullet2 = pygame.image.load("a2_bullet.png")
a1 = pygame.image.load("galaga_a1.png")
a2 = pygame.image.load("galaga_a2.png")
game_over = pygame.image.load("game_over.png")
you_win = pygame.image.load("you_win.png")

#Object creating
play = True
ship = Ship(205, 700)
bullets = []
next = 0
aliens = []
shoots = []
shipblit = False
life = 3
cnt = 0
bcnt = 0
stage = 1
not_first = False
score = 0
instruct = True

#Instruction window
while instruct:
    screen.fill((0, 0, 0))
    inst = font2.render("Intructions:", True, (255, 255, 255))
    i_1 = font2.render("-Hold down right of left arrows to move right.", True, (255, 255, 255))
    i_2 = font2.render("-Press space to shoot", True, (255, 255, 255))
    i_3 = font2.render("There are 3 stages total! Have fun! :D", True, (255, 255, 255))
    i_4 = font2.render("Press Space to Start", True, (255, 255, 255))
    screen.blit(inst, (200, 200))
    screen.blit(i_1, (45, 230))
    screen.blit(i_2, (180, 260))
    screen.blit(i_3, (75, 320))
    screen.blit(i_4, (160, 360))
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                instruct = False
    pygame.display.update()

#Game
while True:
    if play:
        screen.blit(image, (0, 0))
        #Sets aliens for each stage
        if len(aliens) == 0:
            if not_first:
                stage += 1
            if stage == 1:
                for i in range(6):
                    aliens.append(Alien(i * 35, 100, 1))
                for i in range(6):
                    aliens.append(Alien(i * 35, 70, 2))
                not_first = True
            if stage == 2:
                for i in range(6):
                    aliens.append(Alien(i * 35, 100, 1))
                for i in range(6):
                    aliens.append(Alien(i * 35, 70, 2))
                for i in range(6):
                    aliens.append(Alien(i * 35, 40, 2))
            if stage == 3:
                for i in range(6):
                    aliens.append(Alien(i * 35, 100, 2))
                for i in range(6):
                    aliens.append(Alien(i * 35, 70, 2))
                for i in range(6):
                    aliens.append(Alien(i * 35, 40, 2))
            if stage == 4:
                play = False

        #Checks for pygame events and keeps bullets infinite
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    ship.left = True
                if event.key == K_RIGHT:
                    ship.right = True
                if event.key == K_SPACE:
                    bullets.append(Bullet(ship.xPos + 21, ship.yPos, 10))
                    if len(bullets) <= next:
                        next = len(bullets) - 1
                    bullets[next].move = True
                    next += 1
            if event.type == KEYUP:
                if ship.left and event.key == K_LEFT:
                    ship.left = False
                elif ship.right and event.key == K_RIGHT:
                    ship.right = False

        if ship.left:
            ship.moveLeft()
        if ship.right:
            ship.moveRight()

        #Collision detection for ship bullets to aliens
        for a in range(len(aliens)):
            for b in range(len(bullets)):
                if bullets[b].xPos >= aliens[a].xPos and bullets[b].xPos <= aliens[a].xPos + 25 and bullets[b].yPos <= aliens[a].yPos + 20:
                    bullets[b].move = False
                    aliens[a].exist = False

        #Draws ship bullets
        for i in range(len(bullets)):
            if i < len(bullets) and bullets[i].move:
                bullets[i].moveUp()
                screen.blit(bullet1, (bullets[i].xPos, bullets[i].yPos))
            if i < len(bullets) and not bullets[i].move:
                bullets.remove(bullets[i])

        #Draws aliens
        for i in range(len(aliens)):
            if i < len(aliens) and aliens[i].left and aliens[i].exist:
                aliens[i].moveLeft()
            if i < len(aliens) and aliens[i].right and aliens[i].exist:
                aliens[i].moveRight()
            if i < len(aliens) and aliens[i].num == 1 and aliens[i].exist:
                screen.blit(a1, (aliens[i].xPos, aliens[i].yPos))
            if i < len(aliens) and aliens[i].num == 2 and aliens[i].exist:
                screen.blit(a2, (aliens[i].xPos, aliens[i].yPos))
            if i < len(aliens) and not aliens[i].exist:
                if aliens[i].num == 1:
                    score += 50
                if aliens[i].num == 2:
                    score += 75
                aliens.remove(aliens[i])

        #Sets an alien to shoot continuously
        if len(aliens) > 0:
            shoot1 = randint(0, len(aliens) - 1)
            if aliens[shoot1].exist and aliens[shoot1].num == 2:
                shoots.append(Bullet(aliens[shoot1].xPos + 5, aliens[shoot1].yPos + 30, 10))
                shoots[0].move = True

        #Collision detection for alien bullets to ship
        for i in range(len(shoots)):
            if shoots[i].move and ship.exist and shoots[i].xPos >= ship.xPos and shoots[i].xPos <= ship.xPos + 56 and shoots[i].yPos + 15 >= ship.yPos:
                shoots[i].move = False
                ship.exist = False
                life -= 1
                if life == 0:
                    play = False

        #Draws alien bullets forever
        for i in range(len(shoots)):
            if i < len(shoots) and shoots[i].move:
                shoots[i].moveDown()
                screen.blit(bullet2, (shoots[i].xPos, shoots[i].yPos))
            if i < len(shoots) and not shoots[i].move:
                shoots.remove(shoots[i])

        if ship.exist:
            if life == 3:
                screen.blit(s_temp, (0, 770))
                screen.blit(s_temp, (30, 770))
            if life == 2:
                screen.blit(s_temp, (0, 770))
            screen.blit(s, (ship.xPos, ship.yPos))
        elif not ship.exist and life > 0:
            if life < 3:
                if life == 2:
                    screen.blit(s_temp, (0, 770))
                cnt += 1
                if cnt == 30:
                    cnt = 0
                    ship.exist = True
                    screen.blit(s, (ship.xPos, ship.yPos))
        elif not ship.exist and life == 0:
            play = False
        clock.tick(100)
        font = pygame.font.SysFont("Comic Sans MS", 40)
        text = font.render("" + str(score), False, red)
        screen.blit(text, (0, 0))
        pygame.display.update()

    else:
        if not ship.exist:
            screen.blit(game_over, (0, 250))
            clock.tick(100)
        else:
            screen.blit(you_win, (0, 250))
            clock.tick(100)
        temp = font1.render("Play again? Press Backpace", True, red)
        screen.blit(temp, (50, 450))
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    play = True
                    ship = Ship(205, 700)
                    bullets = []
                    next = 0
                    aliens = []
                    shoots = []
                    shipblit = False
                    life = 3
                    cnt = 0
                    bcnt = 0
                    stage = 1
                    not_first = False
                    score = 0

        text = font.render("" + str(score), True, red)
        screen.blit(text, (0, 0))
        pygame.display.update()