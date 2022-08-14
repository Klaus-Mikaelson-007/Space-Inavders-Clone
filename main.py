import pygame
import random
import math

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

playerImage = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

no_of_enemies = 10

for i in range (no_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


missileImage = pygame.image.load('missile.png')
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 1
missile_state = "ready"

score = 0

font = pygame.font.Font('freesansbold.ttf',32)
textX = 310
textY = 10

game_over_textX = 310
game_over_textY = 250
game_over_font = pygame.font.Font('freesansbold.ttf',64)

isScreenRunning = True

def player(x,y):
    screen.blit(playerImage,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImage[i],(x,y))

def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImage,(x+16,y+10))

def isCollided(enemyX,enemyY,missileX,missleY):
    distance = math.sqrt( math.pow((enemyX-missileX),2 ) + math.pow((enemyY-missileY),2) )

    if distance <27:
        return True
    else:
        return False

def show_score(x,y):
    text = font.render("Score : " + str(score),True,(255,255,255))
    screen.blit(text,(x,y))

def game_over(x,y):
    text = font.render("GAME OVER",True,(255,255,255))
    screen.blit(text,(x,y))

while isScreenRunning:

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            isScreenRunning = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change =-0.4
            if event.key == pygame.K_RIGHT:
                playerX_change =0.4
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    missile_sound = mixer.Sound('missile.wav')
                    missile_sound.play()
                    missileX = playerX
                    fire_missile(missileX,missileY)


        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0
    
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    for i in range (no_of_enemies):

        if enemyY[i] > 750:
            for j in range (no_of_enemies):
                enemyY[j] = 2000
            game_over(game_over_textX,game_over_textY)
            break

        enemyX[i] +=enemyX_change [i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] +=enemyY_change[i]

        collision = isCollided(enemyX[i],enemyY[i],missileX,missileY)

        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            missileY = 480
            missile_state = "ready"
            score+=1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)
        


    if missileY<=0:
        missileY = 480
        missile_state = "ready"

    if missile_state is "fire":
        fire_missile(missileX,missileY)
        missileY -=missileY_change


    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update()
