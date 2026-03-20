import random
import pygame
import numpy as np
import math
import matplotlib.pyplot as plt

pygame.init ()

a = 10
width = 1200
height = 800
dt = 1 / 60
m = 3
radius = m * 4
background = pygame.display.set_mode ((width + a, height + a))
run = 1
clock = pygame.time.Clock ()

mu = 0.3
T = 0  # temperatura
print (np.arctan2 (0, 10) * 180 / np.pi)


# viteza = math.sqrt(T)
def rotatie(unghi, x0, y0, x1, y1):
    x = x0 + x1 * round (np.cos (unghi), 2) + round (y1 * np.sin (unghi), 2)
    y = y0 - x1 * round (np.sin (unghi), 2) + round (y1 * np.cos (unghi), 2)
    return x, y


def draw_line(x1, y1, x2, y2):
    pygame.draw.line (background, color="black", start_pos=(x1, y1), end_pos=(x2, y2), width=5)


def switch(a, b):
    c = a
    a = b
    b = c
    return a, b

def norm(v):
    return np.linalg.norm(v)

print(switch((100, 0), (0, 100)))


def tol(x, y, v):
    x -= v[0] * dt
    y -= v[1] *dt
    return x, y


class Ball:

    def __init__(self, mass, x, y, v, culoare):
        self.mass = mass
        self.v = v
        self.x = x
        self.y = y

        self.culoare = culoare




    def ciocnire(self, balls):
        for other in balls:
            if other is not self:

                distanta = math.sqrt(pow ((other.x - self.x), 2) + pow ((other.y - self.y), 2))
                radial_unit = np.array([self.x - other.x, self.y - other.y]) / distanta
                normal_unit = np.array([-radial_unit[1], radial_unit[0]])


                if distanta < (2 * radius):
                    self.x, self.y = tol(self.x, self.y, self.v)
                    other.x, other.y = tol(other.x, other.y, other.v)
                    print ('CIOCNIRE')
                    #cos = np.dot(self.v , radial_unit) / (norm(self.v) * norm(radial_unit))
                    #print("cos: ", cos)
                    relative_velocity = self.v - other.v
                    v_radial = np.dot(radial_unit, relative_velocity) * radial_unit
                    v_normal = np.dot(normal_unit, relative_velocity) * normal_unit
                    #print(v_radial)
                    other.v = v_radial + other.v
                    self.v = -v_radial + self.v
                    #self.v, other.v = switch(self.v, other.v)


    def draw(self):
        pygame.draw.circle(background, center=(self.x, self.y), color=self.culoare, radius=radius)

    def movement(self):

        self.v = self.v - mu*self.v *dt
        vx, vy = self.v[0], self.v[1]


        self.x += vx * dt
        self.y += vy * dt

        ### walls ###

        if not 0 + a < self.x < width:
            self.v[0] *= -1
        if not 0 + a < self.y < height:
            self.v[1] *= -1

        if norm(self.v) < 9:
            self.v = self.v * 0

    def compute_circumference(self, click, mouse_pos):

        dist = math.sqrt (pow ((mouse_pos[0] - self.x), 2) + pow ((mouse_pos[1] - self.y), 2))
        stick_length = 300
        radial_unit = np.array ([(mouse_pos[0] - self.x), (mouse_pos[1] - self.y)]) / dist
        vector = stick_length * radial_unit
        activated = 0

        if dist< 2*radius + 10:
            activated = 1
        circumference0 = np.array ([self.x, self.y]) + radial_unit * radius
        circumference = circumference0

        if click == 0:
            circumference = circumference0* 0
            vector = vector*0
        if click == 1:
            circumference = np.array (mouse_pos) + radial_unit * radius
        if click == 2:
            v_stick = 10
            v = 3 * dist
            circumference = np.array (mouse_pos) + radial_unit * radius



            circumference = circumference - dist/2 * radial_unit
            self.v = - v * radial_unit


        return circumference, vector, activated

    def launch(self, mouse_pos, click):
        if norm(self.v) == 0:
            circumference, vector, activated = self.compute_circumference(click, mouse_pos)

            draw_line(circumference[0], circumference[1], vector[0] + circumference[0], vector[1] + circumference[1])


        #if dist < 2*radius + 3:
            #self.v = np.array([1000, 0])

def move_stick(circumference, radial_unit, ball):
    v_stick = 10
    circumference0 = np.array ([ball.x, ball.y]) + radial_unit * radius
    if norm(circumference - circumference0) > 10:
        circumference = circumference - np.array([v_stick, v_stick]) / 2 * radial_unit

    return circumference


def Kinetic(v):
    return 1/ 2 * m * norm(v)**2


def create_objects(n):
    objects = []
    gap = 2*radius + 2
    viteza = np.array ([0, 0])
    for i in range(0, 5):
        j = i+1
        for k in range(0,j):
            obj = Ball(m, 2*width/3 + (i)*gap, height/2 + (k)*gap - radius * (i), viteza,"black")
            objects.append(obj)
    return objects





ball1 = Ball(m, 100, 300, np.array([100, 0]), "red")
ball2 = Ball(m, 300, 310, np.array([0, 0]), "green")
ball3 = Ball(m, 140, 100, np. array([-200, 100]), "blue")
ball4 = Ball(m, 100, 100, np. array([200, -100]), "black")
x_ball, y_ball = 0, 0


click = 0


#balls = [ball1, ball2]# ball3, ball4]
balls = create_objects(15)

red_ball = Ball(m, width/2 - 200, height/2 + 30, np.array([0, 0]), "red")

balls = np.append(balls, red_ball)
initial = 0
while True:

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = 1

        if event.type == pygame.MOUSEBUTTONUP:
            click = 2


    background.fill ("white")

    total = 0

    for ball in balls:
        ball.draw()
        ball.movement()

        total += Kinetic(ball.v) / len(balls)
        ball.ciocnire (balls)


    print("click: ", click)
    if click == 0 and initial == 0:
        red_ball.x, red_ball.y = pygame.mouse.get_pos()


    red_ball.launch(pygame.mouse.get_pos(), click)
    if click == 2:
        click = 0
        initial = 1
    #print(ball1.v)
    print(total)
    pygame.display.update ()
    clock.tick (60)
