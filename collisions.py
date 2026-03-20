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
m_max = 6

background = pygame.display.set_mode ((width + a, height + a))
run = 1
clock = pygame.time.Clock ()

mu = 0.3
T = 0  # temperatura
print (np.arctan2 (0, 10) * 180 / np.pi)



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


def tol(x, y, over, rad):

    x-= rad[0] * over
    y-= rad[1] * over
    return x, y


class Ball:

    def __init__(self, mass, x, y, v, culoare):
        self.mass = mass
        self.radius = self.mass * 4
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

                #
                if distanta <= (self.radius + other.radius):
                    self.x, self.y = tol (self.x, self.y, over=(self.radius + other.radius) - distanta,
                                          rad=-radial_unit)
                    other.x, other.y = tol (other.x, other.y, over=(self.radius + other.radius) - distanta,
                                            rad=radial_unit)
                #     print ('CIOCNIRE')
                #     relative_v = self.v - other.v
                #     #p_radial = np.dot(radial_unit, relative_p) * radial_unit
                #     other_v = other.v
                #     other.v = (relative_v - normal_unit*np.dot(normal_unit, relative_v)) + other.v
                #     self.v = (normal_unit*np.dot(normal_unit, relative_v)) + other_v
                #


                    print ('CIOCNIRE')

                    relative_p = self.v*self.mass - other.v*other.mass
                    p_radial = np.dot(radial_unit, relative_p) * radial_unit

                    other.v = (2 * other.mass / (other.mass + self.mass) * p_radial + other.v * other.mass)/other.mass
                    self.v = (-2 * self.mass / (other.mass + self.mass) * p_radial + self.v * self.mass)/self.mass



    def draw(self):
        pygame.draw.circle(background, center=(self.x, self.y), color=self.culoare, radius=self.radius)

    def movement(self):

        vx, vy = self.v[0], self.v[1]


        self.x += vx * dt
        self.y += vy * dt

        ### walls ###

        if not 0 + a < self.x < width:
            self.v[0] *= -1
        if not 0 + a < self.y < height:
            self.v[1] *= -1



colors = ["orange", "red", "blue", "black", "green", "yellow", "orange", "pink"]
def create_objects(n, a, colors):
    objects = []
    gap = 120

    for i in range(0, int(np.sqrt(n))):
        for k in range(0,int(np.sqrt(n))):
            m = random.randint(2, m_max)
            viteza = 2*a/m* np.array ([np.random.uniform (-1, 1), np.random.uniform (-1, 1)])
            obj = Ball(m,  width/3 + (i)*gap, height/3 + (k)*gap, viteza, colors[m])
            objects.append(obj)
    return objects

click = 0



balls = create_objects(36, 400, colors)




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
    E = 0
    for ball in balls:
        E += ball.mass * np.dot(ball.v, ball.v)

        ball.draw()
        ball.movement()

        ball.ciocnire (balls)

    print(E)


    #print(ball1.v)

    pygame.display.update ()
    clock.tick (60)
