import random
import pygame
import numpy as np
import math
import matplotlib.pyplot as plt

pygame.init ()


width = 800
height = 800
dt = 1 / 100

mu = 0.
background = pygame.display.set_mode ((width, height))
run = 1
clock = pygame.time.Clock ()

g = 981
T = 0  # temperatura

radius = 10
def tol(x, v):
    x -= v[0] * dt
    return x



def draw_line(p0, p1):
    pygame.draw.line (background, color="black", start_pos=(p0[0], p0[1]), end_pos=(p1[0], p1[1]))


def switch(a, b):
    c = a
    a = b
    b = c
    return a, b

def norm(v):
    return np.linalg.norm(v)

def distance(p0, p1):
    return np.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

print(switch((100, 0), (0, 100)))
class Pendul:

    def __init__(self, m, l, theta, ref):
        self.m = m
        self.l = l
        self.theta = theta
        self.ref = ref


        self.pos = np.array([self.ref[0] + np.sin(self.theta)*self.l, self.ref[1] + np.cos(self.theta)*self.l] )
        self.unit = (self.ref - self.pos) / self.l


        self.acc = 0
        self.omega = 0

    def draw(self):
        pygame.draw.circle(background, center=self.pos, radius=radius, color='red')
        pygame.draw.circle (background, center=self.ref, radius=1, color='black')
        draw_line(self.ref, self.pos)

    def collision(self, pendulums):
        #for index in range(len(pendulums)- 1):
        index = pendulums.index(self)
        if index < len(pendulums)-1:
            other = pendulums[index+1]

            dist = distance(other.pos, self.pos)
            if dist<2*radius:
                print('ciocnire')
                radial_unit = (self.pos - other.pos) / dist
                #self.theta -= self.omega * dt
                # if self.theta < 0.05:
                self.omega, other.omega = other.omega, self.omega
                if np.abs(self.theta)<0.05 and np.abs(other.theta)<0.05:
                    self.theta, other.theta = 0, 0



            #break


    def update(self):
        self.acc = -g/self.l * np.sin(self.theta)
        self.omega += self.acc * dt
        self.theta += self.omega * dt
        self.pos = np.array ([self.ref[0] + np.sin (self.theta) * self.l, self.ref[1] + np.cos (self.theta) * self.l])


        self.draw()

diff = 1e-5

pendul1 = Pendul(1, 300, -np.pi/6 , np.array([width/2, 10]))
pendul2 = Pendul(1, 300, (-np.pi/6 + diff), np.array([width/2 + 2*radius, 10]))
pendul3 = Pendul(1, 300, 0*(-np.pi/6 + 2*diff), np.array([width/2 + 4*radius, 10]))
pendul4 = Pendul(1, 300, 0, np.array([width/2 + 6*radius, 10]))
pendul5 = Pendul(1, 300, 0, np.array([width/2 + 8*radius, 10]))

pendulums = [pendul1, pendul2, pendul3, pendul4, pendul5]
#balls = create_objects(16)
while True:

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = 1

        if event.type == pygame.MOUSEBUTTONUP:
            click = 0

    background.fill ("white")

    for pendul in pendulums:
        pendul.collision(pendulums)
    for pendul in pendulums:
        pendul.update()



    pygame.display.update ()
    clock.tick (120)
