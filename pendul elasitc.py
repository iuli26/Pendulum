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
dt = 1/60
g = 0
mu = 0.5
x_ball = width/2
lungime_initiala = 200
x_ref = x_ball - lungime_initiala *np.sqrt(1)/2
y_ref = height/2
y_ball = y_ref
vX, vY = 0, 0

real = 1         # real =  1 : un resort real
                   # real = 0 : un oscilator armonic



def in_square(point):
    if not x_ech - (lungime_initiala) < point[0]< x_ech + (lungime_initiala) and y_ech - (lungime_initiala) < point[1]< y_ech + (lungime_initiala):
        return 1
    elif x_ech - (lungime_initiala) < point[0]< x_ech + (lungime_initiala) and not y_ech - (lungime_initiala) < point[1]< y_ech + (lungime_initiala):
        return 0
    elif x_ech - (lungime_initiala) < point[0]< x_ech + (lungime_initiala) and y_ech - (lungime_initiala) < point[1]< y_ech + (lungime_initiala):
        return 10
def ball(x_ball, y_ball):
    pygame.draw.circle (background, center=(x_ball, y_ball), color="red", radius=5*m)
    return x_ball, y_ball



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

    def lungime_initiala(self, x_ball, y_ball):
        return np.sqrt ((x_ball - self.x) ** 2 + (y_ball - self.y) ** 2)
    def draw_spring(self, x_ball, y_ball):
        l = self.lungime_initiala(x_ball, y_ball)
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



    def force(self, x_ball, y_ball):
        force = -self.k * (self.lungime_initiala(x_ball, y_ball) - self.l0)
        theta = np.arctan2(y_ball-self.y, x_ball-self.x)

        return np.array([force*np.cos(theta), force*np.sin(theta) + m*g])    #F_x, F_y



def draw_line(x1, y1, x2, y2, grosime):

    pygame.draw.line(background, color="black", width=grosime, start_pos=(x1, y1), end_pos=(x2, y2))



x_ech = x_ball
y_ech = y_ball
k = 20
m = 2
resitence_coeff = 0
x_ball_prev_prev = x_ball

number_of_coils = 10

spring_down = Spring(x_ref + lungime_initiala, y_ref-lungime_initiala, coils=number_of_coils, k=k, x_ech=x_ball, y_ech=y_ball)

springs = [spring_down]

a = 0
press = 0
trajectory_points = []
while True:
    a += 1
    #print("a: ", a)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = 1

        if event.type == pygame.MOUSEBUTTONUP:
            click = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                press = 1
    background.fill("white")
    #axa()

    #if press == 1:
    g = 981
    inrange = []
    for spring in springs:
        inrange.append(spring.draw_spring(x_ball, y_ball))
        #print(inrange)

    ball (x_ball, y_ball)
    if click == 1:
        x_ball, y_ball = pygame.mouse.get_pos()

        x_ball_prev_prev = x_ball
        trajectory_points = []
        # if x_ball < x_ref:
        #     x_ball = x_ref
        vX = 0
        vY = 0
        acc = 0
        #print (acc_x, acc_y)

    if click == 0:
        x_ball_prev = x_ball
        F = 0
        for spring in springs:
            F += spring.force(x_ball, y_ball)
        F_x, F_y = F[0], F[1]
        #print(acc_x, acc_y)
        vX += (F_x - mu*vX)/m*dt
        vY += (F_y - mu*vY)/m * dt

        x_ball += vX * dt
        y_ball += vY * dt
        trajectory_points.append ((x_ball, y_ball))
        for i in range (1, len (trajectory_points)):
            draw_line(trajectory_points[i - 1][0], trajectory_points[i - 1][1], trajectory_points[i][0],
                       trajectory_points[i][1], 1)


    pygame.display.update()
    clock.tick(120)
