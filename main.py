import pygame
import random
import math
from pygame import mixer

# initialize game
pygame.init()

# initialize screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load("background.jpg")

# background music
mixer.init()
mixer.music.load("background.mp3")
mixer.music.play(-1)

# title and thumbnail
pygame.display.set_caption("Covid Invaders")
icon = pygame.image.load("virus.png")
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load("hospital.png")
playerX = 370
playerY = 540
playerX_change = 0
playerY_change = 0

# ENEMIES
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies = 6

# ENEMY BASE
for i in range(enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# BULLET ready or fire
bulletImg = pygame.image.load("medicine.png")
bulletX = 0
bulletY = 540
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

# game score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# game over display
game_over_text = pygame.font.Font('freesansbold.ttf', 64)


# game over function
def game_over():
    game_over_font = game_over_text.render(f'GAME OVER', True, (0, 0, 0))
    screen.blit(game_over_font, (200, 250))


# score function
def score(x, y):
    scores = font.render(f'Score: {score_value}', True, (0, 0, 0))
    screen.blit(scores, (x, y))


# player function
def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy one function
def enemy1(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# fire bullet
def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


#             ___________________
# Distance = \/(x2−x1)^2+(y2−y1)^2
def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 29:
        return True
    return False


# GAME Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    # loop over events
    for event in pygame.event.get():
        # check if window closed
        if event.type == pygame.QUIT:
            running = False

        # key event check if key down
        if event.type == pygame.KEYDOWN:
            # check if key down is left
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            # check if key down is right
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            # check if key down is space bar
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    mixer.init()
                    mixer.music.load("shot.mp3")
                    mixer.music.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)

        # check if event is key up
        if event.type == pygame.KEYUP:
            # check if key up is left/right
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change
    playerY += playerY_change

    # player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 735:
        playerX = 735
    if playerY <= 0:
        playerY = 0
    elif playerY >= 535:
        playerY = 535

    # iterate through enemies
    for i in range(enemies):
        # Game Over
        if enemyY[i] > 480:
            for j in range(enemies):
                enemyY[j] = 2000
            game_over()
            break

        # enemy movement
        enemyX[i] += enemyX_change[i]

        # enemy boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 735:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 3
        if enemyY[i] >= 535:
            enemyY_change[i] = -3

        # bullet collision
        collisions = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisions:
            mixer.music.load('explosion.mp3')
            mixer.music.play()
            bulletY = 540
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # draw enemies
        enemy1(enemyX[i], enemyY[i], i)

    # bullet reset
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet movement
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # draw player
    player(playerX, playerY)

    # draw score
    score(text_x, text_y)

    # update display
    pygame.display.update()
