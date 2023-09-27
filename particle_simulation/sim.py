import numpy as np
from pygame.locals import KEYDOWN, K_ESCAPE
import pygame


pygame.init()


# set up the UI
space_size = 500
screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()

running = True

# Set up the particle attributes

mass1 = 5
x1 = np.random.randint(space_size) # x1 initial condition
y1 = np.random.randint(space_size) # y1 initial condition
x1v = 100 # Initial  x1 dot
y1v = 1250 # Initial  y1 dot
radius1 = 10
color1 = (255, 0, 0)

mass2 = 10
x2 = np.random.randint(space_size) # x1 initial condition
y2 = np.random.randint(space_size) # y1 initial condition
x2v = 100 # Initial  x2 dot
y2v = 125 # Initial  y2 dot
radius2 = 20
color2 = (0, 0, 255)

rate = 60 #Frames per second
dt = 1 / rate #Seconds per frame (time step between frames)
radius = 10
color = (255, 0, 0)

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, color1, (x1, y1), radius1)

    pygame.draw.circle(screen, color2, (x2, y2), radius2)

    pygame.display.flip()

    # Particle 1 dynamics
    x1 = x1 + x1v * dt
    y1 = y1 + y1v * dt

    # Particle 2 dynamics
    x2 = x2 + x2v * dt
    y2 = y2 + y2v * dt

    # Wall collision mechanics
    if ((x1 - radius) < 0) or ((x1 + radius) > space_size):
        x1v = -x1v
    if ((y1 - radius) < 0) or ((y1 + radius) > space_size):
        y1v = -y1v
    if ((x2 - radius) < 0) or ((x2 + radius) > space_size):
        x2v = -x2v
    if ((y2 - radius) < 0) or ((y2 + radius) > space_size):
        y2v = -y2v

    # Particle collision mechanics
    if (abs(x2 - x1) < (radius1 + radius2)):
        # TODO implement 2D collision logic using sprites / groups. For now just doing something basic
        y1v, y2v = y2v, y1v
        x1v, x2v = x2v, x1v
    
    clock.tick(rate)

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:

                running = False

pygame.quit()
