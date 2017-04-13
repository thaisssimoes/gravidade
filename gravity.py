import pygame
import sys
import random
import math

#Constantes
HEIGHT = 800
WIDTH = 800
WINDOWSIZE = (WIDTH, HEIGHT)
GRAVITY = 0.002
DRAG = 0.999
ELASTICITY = 0.75

#Variaveis
red=255
green=255
blue=255
backgroundColor = (red, green, blue)



def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) *length1 + math.sin(angle2) * length2
    y = math.cos(angle1) *length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y,x)
    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y)<= p.size:
            return p
    return None

class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (red-255, green-255, blue)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, math.pi, GRAVITY)
        self.x +=  math.sin(self.angle)*self.speed
        self.y -=  math.cos(self.angle)*self.speed
        self.speed *= DRAG

    def bounce(self):
        if self.x > WIDTH - self.size:
            self.x = 2 * (WIDTH-self.size) - self.x
            self.angle = - self.angle
            self.speed *= ELASTICITY

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= ELASTICITY

        if self.y > HEIGHT - self.size:
            self.y = 2*(HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY


screen = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Gravity")

numberOfParticles = 10
myParticles=[]

for number in range(numberOfParticles):

    size = random.randint(10,20)
    x = random.randint(size, WIDTH - size)
    y = random.randint(size, HEIGHT - size)

    randomParticles = Particle(x, y, size)
    randomParticles.speed = random.random()
    randomParticles.angle = random.uniform(0, math.pi*2)

    myParticles.append(randomParticles)

selectedParticle = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selectedParticle = findParticle(myParticles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedParticle = None

    screen.fill(backgroundColor)

    if selectedParticle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selectedParticle.x
        dy = mouseY - selectedParticle.y
        selectedParticle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selectedParticle.speed = math.hypot(dx, dy) * 0.1

    for particles in myParticles:
        particles.move()
        particles.bounce()
        particles.display()

    pygame.display.flip()
