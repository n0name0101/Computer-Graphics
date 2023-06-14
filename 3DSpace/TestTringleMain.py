import pygame
from pygame.locals import *
import math
import numpy as np

#Own Library
from Model import *
from Vector2 import *
from Vector3 import *
from Triangle import *
from GeneralProjection import *

def twoDToPyGame(twoD , pyObject):
    screen_info = pyObject.display.Info()
    return Vector2(twoD.x + screen_info.current_w/2.0,screen_info.current_h/2.0 - twoD.y)

objCam = Vector3(0,0,0)
objLookAt = Vector3(0,0,1)
objUp = Vector3(0,1,0)

yaw = 0.0
pitch = 0.0
CAMROTSPEED = math.radians(1)
PITCHLIM = math.radians(80)

modelList = []
modelList.append(Model(50,Vector3(0,0,200)))
modelList.append(Model(50,Vector3(200,0,0)))
modelList.append(Model(50,Vector3(200,0,100)))
modelList.append(Model(50,Vector3(-200,0,100)))
modelList.append(Model(50,Vector3(0,0,-200)))
modelList.append(Model(50,Vector3(200,0,-200)))

speed = 0.9

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width = 1280
height = 720

# Create the screen
#screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height),RESIZABLE)

# Set the color of the rectangle
color = (255, 0, 0)  # Red color

# Set the position and size of the rectangle
x = 0
y = 0
rect_width = 200
rect_height = 100

# Main game loop
running = True

# Variables to track key states
key_w_pressed = False
key_a_pressed = False
key_s_pressed = False
key_d_pressed = False

angle_x = 0
angle_y = 0
angle_z = 0

# Create a Clock object
clock = pygame.time.Clock()
print('Start')
print('Back')
V1 = Vector2(0,4)*50
V2 = Vector2(2,1)*50
V3 = Vector2(-2,1)*50
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    key_w_pressed = True
                elif event.key == pygame.K_a:
                    key_a_pressed = True
                elif event.key == pygame.K_s:
                    key_s_pressed = True
                elif event.key == pygame.K_d:
                    key_d_pressed = True
                elif event.key == pygame.K_LSHIFT:
                    speed = 1.9
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    key_w_pressed = False
                elif event.key == pygame.K_a:
                    key_a_pressed = False
                elif event.key == pygame.K_s:
                    key_s_pressed = False
                elif event.key == pygame.K_d:
                    key_d_pressed = False
                elif event.key == pygame.K_LSHIFT:
                    speed = 0.9
    # Update the display
    screen.fill((255, 255, 255))  # Black color
    if key_w_pressed :
        V1 = V1.rotate(1)
        V2 = V2.rotate(1)
        V3 = V3.rotate(1)
    #if compare(V2,V1) : V1 , V2 = swap(V1,V2)
    #if compare(V3,V1) : _ver1 , _ver2 = swap(V1,V2)
    #if compare(_ver2,_ver3) : _ver2 , _ver3 = swap(_ver2,_ver3)
    V1P = twoDToPyGame(V1,pygame)
    V2P = twoDToPyGame(V2,pygame)
    V3P = twoDToPyGame(V3,pygame)
    pygame.draw.circle(screen, (255,0,0), (V1P.x,V1P.y) , 5)
    pygame.draw.circle(screen, (255,0,0), (V2P.x,V2P.y) , 5)
    pygame.draw.circle(screen, (255,0,0), (V3P.x,V3P.y) , 5)
    drawTriangle(screen,V1P,V2P,V3P)
    pygame.display.flip()
    # Limit the frame rate
    clock.tick(60)
# Quit the game
pygame.quit()
