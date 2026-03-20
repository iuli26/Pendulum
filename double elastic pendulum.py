import pygame
import numpy as np
import math
import matplotlib.pyplot as plt
pygame.init()


width = 1280
height = 800
background = pygame.display.set_mode((width, height))
run = 1
clock = pygame.time.Clock()

click = 0
dt = 1 / 60
g = 981

x_ball = width/3
lungime_initiala = 200
x_ref = x_ball - lungime_initiala
y_ref = height/2
y_ball = y_ref
vX, vY = 0, 0

real = 1         # real =  1 : un resort real
                   # real = 0 : un oscilator armonic


def ball(x_ball, y_ball):
    pygame.draw.circle (background, center=(x_ball, y_ball), color="red", radius=5*m)
    return x_ball, y_ball


class Ball:
    def __init__(self, x, y, v, m, color):
        self.x = x
        self.y = y
        self.vx = v[0]
        self.vy = v[1]
        self.m = m
        self.color = color
    def draw(self):
        pygame.draw.circle(background, center=(self.x, self.y), color=self.color, radius=10 * m)
        return self.x, self.y

    def motion(self, F):
        F_x, F_y = F[0], F[1]
        self.vx += (F_x - mu*self.vx)/self.m * dt
        self.vy += (F_y - mu*self.vy)/self.m * dt

        self.x += self.vx * dt
        self.y += self.vy * dt



class Spring_mid:
    def __init__(self, ball_left, ball_right, coils, k):
        self.ball1 = ball_left
        self.ball2 = ball_right
        self.coils = coils
        self.k = k

        x1, y1 = self.ball1.x, self.ball1.y
        x2, y2 = self.ball2.x, self.ball2.y
        self.l0 = np.sqrt ((x1 - x2) ** 2 + (y1 - y2) ** 2)
        self.unit_vec_initial = ((x1-x2) / self.l0, (y1 - y2) / self.l0)
        print(self.l0)
    def lungime(self, ball1, ball2):
        return np.sqrt ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)

    def draw_spring(self, ball1, ball2):
        l = self.lungime (ball1, ball2)
        print(l)
        unit_vec = ((ball1.x - ball2.x) / l, (ball1.y - ball2.y) / l)
        # print(unit_vec)
        normal_vec = (-unit_vec[1], unit_vec[0])
        # print (normal_vec)

        #pygame.draw.circle (background, center=(self.x, self.y), color="black", radius=3)
        n = 300
        points = []
        arr = np.linspace (0, l, n)
        sinus = 5 * np.sin (2 * np.pi * self.coils / l * arr)
        for i in range (n):
            points.append ((ball2.x + arr[i] * unit_vec[0] + sinus[i] * normal_vec[0],
                            ball2.y + arr[i] * unit_vec[1] + sinus[i] * normal_vec[1]))
        pygame.draw.lines (background, 'black', False, points, 2)
        if unit_vec[1] * self.unit_vec_initial[1] + unit_vec[0] * self.unit_vec_initial[0] < 0:
            return 1
        else:
            return 0

    def force(self, ball1, ball2):
        force = -self.k * (self.lungime(ball1, ball2) - self.l0)
        theta = np.arctan2(ball2.y - ball1.y, ball2.x - ball1.x)

        return np.array([force * np.cos (theta), force * np.sin (theta) + m*g])  # F_x, F_y


class Spring:
    def __init__(self, x, y, coils, k, x_ech, y_ech):
        self.x = x
        self.y = y
        self.coils = coils
        self.k = k
        self.x_ech = x_ech
        self.y_ech = y_ech
        self.l0 = np.sqrt((self.x-self.x_ech)**2 + (self.y_ech-self.y)**2)
        self.unit_vec_initial = ((self.x_ech-self.x)/self.l0, (self.y_ech-self.y)/self.l0)

    def lungime(self, x_ball, y_ball):
        return np.sqrt ((x_ball - self.x) ** 2 + (y_ball - self.y) ** 2)
    def draw_spring(self, x_ball, y_ball):
        l = self.lungime(x_ball, y_ball)

        unit_vec = ((x_ball-self.x) / l, (y_ball-self.y)/l)
        #print(unit_vec)
        normal_vec = (-unit_vec[1], unit_vec[0])
        #print (normal_vec)


        pygame.draw.circle(background, center=(self.x, self.y), color="black", radius=3)
        n = 300
        points = []
        arr = np.linspace(0, l, n)
        sinus = 5 * np.sin(2*np.pi*self.coils/l*arr)
        for i in range(n):
            points.append((self.x + arr[i]*unit_vec[0] + sinus[i]*normal_vec[0], self.y + arr[i]*unit_vec[1] + sinus[i]*normal_vec[1]))
        pygame.draw.lines(background, 'black', False, points, 2)
        if unit_vec[1] * self.unit_vec_initial[1] + unit_vec[0] * self.unit_vec_initial[0] < 0:
            return 1
        else: return 0



    def force(self, ball2, ball):
        force = -self.k * (self.lungime(ball.x, ball.y) - self.l0)
        theta = np.arctan2(ball.y-self.y, ball.x-self.x)

        return np.array([force*np.cos(theta), force*np.sin(theta) + m*g])    #F_x, F_y



def draw_line(x1, y1, x2, y2):
    grosime = 2
    pygame.draw.line(background, color="black", width=grosime, start_pos=(x1, y1), end_pos=(x2, y2))



x_ech = x_ball
y_ech = y_ball
k = 20
m = 1
resitence_coeff = 0
x_ball_prev_prev = x_ball

number_of_coils = 20


ball1 = Ball(width/2, height/2, [0, 0], m, "red")
ball2 = Ball(ball1.x, ball1.y+50, [0, 0], m, "green")

spring_up = Spring(width/2, 100, coils=number_of_coils, k=k, x_ech=ball1.x, y_ech=ball1.y)

spring_mid = Spring_mid(ball1, ball2, coils=number_of_coils, k=k)

mu = 0

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
    #axa()
    spring_up.draw_spring(ball1.x, ball1.y)

    spring_mid.draw_spring(ball1, ball2)
    ball1.draw()
    ball2.draw()
    if click == 1:

        #ball1.x = pygame.mouse.get_pos()[0]
        #ball2.x = width - ball1.x
        ball1.x, ball1.y = pygame.mouse.get_pos()
        #ball2.x, ball2.y = ball1.x + 100, ball1.y


        ball1.vx, ball1.vy = 0, 0
        ball2.vx, ball2.vy = 0, 0

    if click == 0:

        F1, F2 = 0, 0
        for spring in [spring_mid, spring_up]:
            F1 += spring.force(ball2, ball1)
        for spring in [spring_mid]:
            F2 += spring.force(ball1, ball2)
        #print(acc_x, acc_y)
        ball1.motion(F1)
        ball2.motion(F2)



    pygame.display.update()
    clock.tick(60)
