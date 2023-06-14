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

while running:
    # Handle events
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

    if key_w_pressed:
        objCam += objLookAt*speed
    elif key_s_pressed:
        objCam -= objLookAt*speed
    elif key_a_pressed:
        objCam += objLookAt.cross(objUp).normalize()*speed
    elif key_d_pressed:
        objCam -= objLookAt.cross(objUp).normalize()*speed


    #Mouse
    if pygame.mouse.get_pressed()[0]:
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
    x , y = pygame.mouse.get_rel()
    if(x < 0):
        yaw -= CAMROTSPEED
    elif(x > 0):
        yaw = ((CAMROTSPEED+yaw) % (2 * math.pi))
    if(y < 0):
        if pitch < PITCHLIM :
            pitch += CAMROTSPEED
    elif(y > 0):
        if pitch > -PITCHLIM :
            pitch -= CAMROTSPEED
    if(y!=0 or x!=0):
        objLookAt.x = np.cos(pitch)*np.sin(yaw)
        objLookAt.y = np.sin(pitch)
        objLookAt.z = np.cos(pitch)*np.cos(yaw)
        objLookAt = objLookAt.normalize()
        model.draw(screen,pygame,objCam,objLookAt,objUp)


    #Update Screen

    #angle_x = (angle_x+1) % 360
    #objModel1.setangle_x(math.radians(angle_x))
    # Clear the screen
    screen.fill((255, 255, 255))  # Black color

    #Sorting Model
    def sortingRule(n) :
        viewMatrix = getViewMat(objCam,objCam+objLookAt,objUp)
        objPosition = n.position.getlist()
        objPosition.append(1)
        objPosition = np.array(objPosition)
        objPosition = objPosition.transpose()
        objPosition = np.dot(viewMatrix,objPosition)
        return objPosition[2]
    modelList.sort(key=sortingRule,reverse=True)

    # Draw the Model
    for model in modelList :
        model.draw(screen,pygame,objCam,objLookAt,objUp)

    # Update the display
    pygame.display.flip()
    # Limit the frame rate
    clock.tick(133)

# Quit the game
pygame.quit()
