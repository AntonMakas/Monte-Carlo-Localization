import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1000, 700), flags=pygame.NOFRAME) #flags=pygame.NOFRAME #pygame.RESIZABLE
pygame.display.set_caption("Monte Carlo Localization")
icon = pygame.image.load('images/Robot_Logo.png')
pygame.display.set_icon(icon)

x = 200
y = 200

width = 30
height = 30

vel = 0.2

obstacles = []
for i in range(20):  # You can adjust the number of obstacles
    rand_landmark = random.randint(0, 1)
    ObsX = random.randint(50, 950)
    ObsY = random.randint(50, 650)
    ObsWidth = 20
    ObsHeight = 20
    if rand_landmark == 0:  # Rectangle
        obstacles.append(('rect', (ObsX, ObsY, ObsWidth, ObsHeight)))
    else:  # Circle
        obstacles.append(('circle', (ObsX, ObsY, ObsWidth)))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('grey')
    for obs in obstacles:
        if obs[0] == 'rect':
            pygame.draw.rect(screen, 'blue', obs[1])
        elif obs[0] == 'circle':
            pygame.draw.circle(screen, 'blue', (obs[1][0], obs[1][1]), obs[1][2])




    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 0:
        x = x - vel
    if keys[pygame.K_RIGHT] and x < screen.get_width()-width:
        x = x + vel
    if keys[pygame.K_DOWN] and y < screen.get_height()-height:
        y = y + vel
    if keys[pygame.K_UP] and y > 0:
        y = y - vel

    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))

    pygame.display.update()

pygame.quit()
