# SPACE INVADER
import math
import pygame
from pygame import mixer
import random

'''INITIALISATION
............................................................'''

pygame.init() # initialise pygame

height = 600
width = 800

screen = pygame.display.set_mode((width, height))                       # create screen

'''
..............................................................'''


'''CAPTION BACKGROUND IMAGE/MUSIC AND ICON
..............................................................'''
#APPEARANCE (TITLE, ICON, IMAGE)
pygame.display.set_caption("Space Invaders")                            # CAPTION/TITLE 
icon = pygame.image.load('ufo.png')                                     # ICON
pygame.display.set_icon(icon)                                           # SET ICON
background = pygame.image.load('background4.jpg')                        # background img

#BACKGROUND SOUNDS
mixer.music.load('5_5_3.mp3')
mixer.music.play(-1)#loop the sound

'''
...............................................................'''



'''GAME CHARACTERS AND OBJECT FEATURES
...............................................................'''

# PLAYER
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# PLAYER FUNCTION
def player(x, y):
    screen.blit(playerImg, (x, y))

# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

for i in range(numOfEnemies):    
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2.5)
    enemyY_change.append(40)

# ENEMY FUNCTION
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 0
bulletState = "ready"                                                   # bullet not visible on screen (state of constant)

# BULLET FUNCTION
def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y +  10))

# BULLET VERTICAL POSITION FUNCTION     
def bulletVertical():
    global bulletY
    bulletY = playerY + 30

# COLLISION BETWEEN BULLET AND ENEMY
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    
    if distance < 27:
        return True
    else:
        return False


# PROPERTIES BEFORE DISPLAYING THE SCORE
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# SHOW SCORE FUNCTION
def showScore(x, y):
    score = font.render('Score : ' + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


# GAME OVER
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)
overTextX = 200
overTextY = 250

#GAME OVER TEXT FUNCTION
def gameOverText(x, y):
    overText = gameOverFont.render('GAME OVER !!!', True, (255, 255, 255))
    screen.blit(overText, (x, y))
    
'''
.............................................................'''




'''GAME LOOP
..............................................................'''

running = True

while running:
    screen.fill((0, 0, 0))                                              # RGB value of screen
    screen.blit(background, (0, 0))                                     # add background image


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        
        # CHECK IF EVENT IS A KEY PRESSED
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change = -3.5                                   # move player to the left
            
            elif event.key == pygame.K_RIGHT:
                playerX_change = 3.5                                    # move player to the right
            
            elif event.key == pygame.K_UP:
                playerY_change = -1                                     # move player up
            
            elif event.key == pygame.K_DOWN:
                playerY_change = 1                                      # move player down
            
            elif event.key == pygame.K_SPACE:
                if bulletState is "ready": 
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletVertical() 
                    bulletX = playerX                                   # Get current X_Coordinate of spaceship
                    fire_bullet(bulletX, bulletY)                       # bullet function when space key is pressed
                    bulletY_change += 12
                
        # CHECK IF A KEY IS RELEASED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0                                      # stop movement
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0                                      # stop movement
   
    # PLAYER MOVEMENT
    playerX += playerX_change
    
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    playerY += playerY_change
    
    if playerY < 0:
        playerY = 0
    if playerY > 536:
        playerY = 536
    
        
    player(playerX, playerY)
    #............................................
    
    # ENEMY MOVEMENT
    for i in range (numOfEnemies):
        
        #GAME OVER......................
        if enemyY[i] > 480:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText(overTextX, overTextY)
            break
        #...............................
        
        
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] < 0:
            enemyX_change[i] = 2.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2.5
            enemyY[i] += enemyY_change[i]
        # COLLISION 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.play()
            bulletVertical()
            bulletState = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)
    # ...........................................
    
    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
        bulletY_change = 0
        
    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    # ............................................  

    # DISPLAYING THE SCORE
    showScore(textX, textY)
    
        
    pygame.display.update()





'''
...................................................................

END

'''  