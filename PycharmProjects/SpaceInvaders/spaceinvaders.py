import pygame
import random
import math
from pygame import mixer

# inicializando o pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background1.png')

# Colocando o título na tela e o ícone
pygame.display.set_caption('Pacverse')
# para colocar um icone no display
# icon = pygame.image.load('')
# pygame.display.set_icon()

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# player
playerimg = pygame.image.load('player.png')
playerx = 370
playery = 480
playerx_change = 0
playery_change = 0

# inimigo
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
numbers_enemies = 6
for i in range(numbers_enemies):
    enemyimg.append(pygame.image.load('ufo.png'))
    # With the random, the enemy shows up in everywhere
    enemyx.append(random.randint(0, 730))
    enemyy.append(random.randint(0, 150))
    enemyx_change.append(0.5)
    enemyy_change.append(40)

# bullet
# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 1
bullet_state = 'ready'


# Função que vai inserir o player na tela(screen.blit)
def player(x, y):
    # coordenadas de onde o player vai iniciar
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    # coordenadas de onde o inimigo vai iniciar
    screen.blit(enemyimg[i], (x, y))


def bullet_fire(x, y):
    # use 'global' to acess the bullet state inside of the fuction
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))


def iscolision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    game_over = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# Game loop
running = True
while running:
    # RGB - Red, Green, Blue - pesquisar RGB no google
    # background color
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether its rigth or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerx_change = -1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # usando um if, a bala só vai ser atirada se estiver no estado pronto
                if bullet_state is 'ready':
                    bulletx = playerx
                    bullet_fire(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # the player stop and wait a new direction
                playerx_change = 0
    # 5 = 5 + -0.1
    # 5 = 5 + 0.1
    playerx += playerx_change

    # create boundaries for the player
    if playerx <= 0:
        playerx = 0
    elif playerx >= 730:
        playerx = 730

    # create boundaries for the enemy movement in x-direction
    for i in range(numbers_enemies):
        # Game Over
        if enemyy[i] > 440:
            for j in range(numbers_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] += 0.5
        elif enemyx[i] >= 730:
            enemyx_change[i] += -0.5
        # create boundaries for the enemy movement in y-direction
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 730:
            enemyx_change[i] = -0.5
            enemyy[i] += enemyy_change[i]

        # Colision
        colision = iscolision(enemyx[i], enemyy[i], bulletx, bullety)
        if colision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = 'ready'
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(0, 150)
            score_value += 1

        enemy(enemyx[i], enemyy[i], i)

    # Bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        bullet_fire(bulletx, bullety)
        bullety -= bullety_change

    show_score(textx, texty)
    player(playerx, playery)
    pygame.display.update()
