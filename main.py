import pygame
import numpy as np
import math

pygame.init()

lungime = 1280
inaltime = 800
background = pygame.display.set_mode((lungime, inaltime))
run = 1
clock = pygame.time.Clock()

click = 0
dt = 1 / 60
g = 981

x_ref = lungime / 2
y_ref = 100
x_ball, y_ball = x_ref + 200, y_ref + 200


def f(y, lungime):
    return g * np.sin(y) / lungime


def euler(i, y1, y, t, l):
    y1.append(y1[i - 1] - f(y[i - 1], l) * dt)
    y.append (y[i - 1] + y1[i] * dt)
    t.append (t[i - 1] + dt)


def ball(x_ball, y_ball):
    pygame.draw.circle (background, center=(x_ball, y_ball), color="black", radius=10)
    return x_ball, y_ball


def axa():
    pygame.draw.line(background, color="black", start_pos=(lungime / 2, 0), end_pos=(lungime / 2, inaltime))


def punct_ref():
    pygame.draw.circle(background, center=(x_ref, y_ref), color="red", radius=3)
    return x_ref, y_ref


def draw_line(x1, y1, x2, y2):
    pygame.draw.line(background, color="black", start_pos=(x1, y1), end_pos=(x2, y2))


def urma(x, y):
    pygame.draw.circle(background, center=(x, y), color="red", radius=3)


def ipotenuza(x_ball, y_ball, x_ref, y_ref):
    ipotenuza = math.sqrt(math.pow((x_ball - x_ref), 2) + math.pow((y_ball - y_ref), 2))
    return ipotenuza


l = ipotenuza(x_ball, y_ball, x_ref, y_ref)
distantaX = x_ball - x_ref
theta = (np.arcsin(distantaX / l))
print(theta)
theta_vector = [theta]
omega_vector = [0]
timp = [0]
index = 1
print(distantaX)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = 1

        if event.type == pygame.MOUSEBUTTONUP:
            click = 0

    background.fill("white")
    axa()

    if click == 1:
        x_ball, y_ball = pygame.mouse.get_pos()
        l = ipotenuza(x_ball, y_ball, x_ref, y_ref)
        distantaX = x_ball - x_ref
        theta = (np.arcsin(distantaX / l))
        theta_vector = [theta]
        omega_vector = [0]
        timp = [0]
        index = 1

    ball(x_ball, y_ball)
    punct_ref()
    draw_line(x_ref, y_ref, x_ball, y_ball)
    draw_line(x_ref, y_ball, x_ball, y_ball)

    if click == 0:
        euler(index, omega_vector, theta_vector, timp, l)
        x_ball = x_ref + l * np.sin(theta_vector[index])
        y_ball = l * np.cos(theta_vector[index]) + y_ref
        print(np.sin(theta_vector[index]), x_ball-x_ref,  ipotenuza(x_ball, y_ball, x_ref, y_ref))
        index += 1
        
    pygame.display.update()
    clock.tick(60)
