import pygame
import random

FPS = 60
W = 300  # ширина экрана
H = 300  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

radius = 10
speed = 3
x, y = W // 2, H + radius
y_start = H + radius
x_start = 0

fire = False
play = True  # Переменная для включения главного цикла

pygame.init()
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

while play:
    sc.fill(BLACK)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            play = False
            pygame.quit()
            break
        if i.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            y = pos[1]
            x = pos[0]
            y_start = H + radius
            x_start = random.randint(0, W)
            fire = True

    if fire:
        if x_start < x:
            x_start += speed
        elif x_start > x:
            x_start -= speed
    if fire:
        if y_start < y:
            y_start += speed
        if y_start > y:
            y_start -= speed
    if fire:
        pygame.draw.circle(sc, BLUE, (x_start, y_start), radius)
    if x_start == x and y_start == y:
        fire = False
        pygame.draw.rect(sc, RED, (pos[0] - 10, pos[1] - 10, 20, 20))
    pygame.display.update()

    clock.tick(FPS)