
import pygame
import numpy as np
import moderngl as mgl
import glm
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# MyCode
from World3D import World3D
from Cube import Cube
from utils import *

# Define constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def get_shader_program(shader_name , ctx) :
    with open(f'Shaders/{shader_name}.vert') as file :
        vertex_shader = file.read()
    with open(f'Shaders/{shader_name}.frag') as file :
        fragment_shader = file.read()
    program = ctx.program(vertex_shader=vertex_shader,fragment_shader=fragment_shader)
    return program

def main():
    move_forward = False
    move_backward = False
    move_left = False
    move_right = False
    cursor_visible = True

    #Pygame INIT
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('Cube Physic')
    clock = pygame.time.Clock()

    #OpenGL INIT
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    ctx = mgl.create_context()
    m_proj = glm.perspective(glm.radians(90), (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 10000.0)

    #For Cube
    cube_shader_program = get_shader_program('default', ctx)
    cube_shader_program['m_proj'].write(m_proj)
    texture = pygame.image.load('textures/img_2.png')
    texture = pygame.transform.flip(texture,flip_x=True , flip_y=True)
    texture = ctx.texture(size=texture.get_size() , components=3,
                        data=pygame.image.tostring(texture,'RGB'))
    cube_shader_program['u_texture_0'] = 0

    #For Contact Point
    contact_point_shader_program = get_shader_program("contact_point",ctx)
    contact_point_shader_program['m_proj'].write(m_proj)

    #3D World INIT
    ThreeDWorld = World3D(SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT), camera=np.array([0, -2000, -100]),lookat=np.array([0, 0, 1]))

    # Add Cube
    ThreeDWorld.add_cube(Cube(x=np.array([0, 2000, 600]), size=(100, 100), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))
    ThreeDWorld.add_cube(Cube(x=np.array([0, -1100 , 600]), size=(0, 0), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))
    ThreeDWorld.add_cube(Cube(x=np.array([0, 4000, 600]), size=(0, 0), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))
    #ThreeDWorld.add_cube(Cube(x=np.array([-300, 0, 0]), size=(100, 100), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))
    #ThreeDWorld.add_cube(Cube(x=np.array([300, 0, 300]), size=(100, 100), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))
    #ThreeDWorld.add_cube(Cube(x=np.array([300, 0, 300]), size=(100, 100), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))
    ThreeDWorld.add_cube(Cube(physic=False, x=np.array([0, -7000, 2000]), size=(8000, 8000), SCREEN_SIZE=(SCREEN_WIDTH, SCREEN_HEIGHT)))  # Terrain
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    cursor_visible = not cursor_visible
                    pygame.mouse.set_visible(cursor_visible)
                    if cursor_visible:
                        pygame.event.set_grab(False)  # Release the mouse grab
                elif event.key == K_w:  # Move camera forward
                    move_forward = True
                elif event.key == K_s:  # Move camera backward
                    move_backward = True
                elif event.key == K_a:  # Move camera left
                    move_left = True
                elif event.key == K_d:  # Move camera right
                    move_right = True
                elif event.key == K_UP:  # Move camera right
                    ThreeDWorld.cubes[ThreeDWorld.controlcube].x = ThreeDWorld.cubes[ThreeDWorld.controlcube].x + ThreeDWorld.cubes[ThreeDWorld.controlcube].forward * 10
                elif event.key == K_DOWN:  # Move camera right
                    ThreeDWorld.cubes[ThreeDWorld.controlcube].x = ThreeDWorld.cubes[ThreeDWorld.controlcube].x - ThreeDWorld.cubes[ThreeDWorld.controlcube].forward * 10
                elif event.key == K_RIGHT:  # Move camera right
                    ThreeDWorld.cubes[ThreeDWorld.controlcube].x = ThreeDWorld.cubes[ThreeDWorld.controlcube].x + ThreeDWorld.cubes[ThreeDWorld.controlcube].right * 10
                elif event.key == K_LEFT:  # Move camera right
                    ThreeDWorld.cubes[ThreeDWorld.controlcube].x = ThreeDWorld.cubes[ThreeDWorld.controlcube].x - ThreeDWorld.cubes[ThreeDWorld.controlcube].right * 10
                elif event.key == K_c:  # Move camera right
                    ThreeDWorld.controlcube = (ThreeDWorld.controlcube+1) % len(ThreeDWorld.cubes)
            elif event.type == KEYUP:
                if event.key == K_w:  # Stop moving camera forward
                    move_forward = False
                elif event.key == K_s:  # Stop moving camera backward
                    move_backward = False
                elif event.key == K_a:  # Stop moving camera left
                    move_left = False
                elif event.key == K_d:  # Stop moving camera right
                    move_right = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)  # Grab the mouse to lock it within the window

        # Move the camera based on the movement flags
        if move_forward:
            ThreeDWorld.camera.pos = ThreeDWorld.camera.pos+ThreeDWorld.camera.lookat * 10
        if move_backward:
            ThreeDWorld.camera.pos = ThreeDWorld.camera.pos-ThreeDWorld.camera.lookat * 10
        if move_left:
            ThreeDWorld.camera.pos = ThreeDWorld.camera.pos+np.cross(ThreeDWorld.camera.lookat, np.array([0, 1, 0])) * 10
        if move_right:
            ThreeDWorld.camera.pos = ThreeDWorld.camera.pos-np.cross(ThreeDWorld.camera.lookat, np.array([0, 1, 0])) * 10

        # Lock cursor within the window
        if not cursor_visible :
            pygame.mouse.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        rel = pygame.mouse.get_rel()
        rotation_speed = 0.1
        ThreeDWorld.camera_lookat_rotation(-rel[1] * rotation_speed, rel[0] * rotation_speed)

        ctx.clear(color=(0.08,0.16,0.18))     
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glRotatef(1, 3, 1, 1)
        
        # Draw World
        ThreeDWorld.drawOpenGLOptimize(ctx , cube_shader_program ,texture)
        # Update World
        ThreeDWorld.step(1 / 120,ctx ,contact_point_shader_program)

        # Calculate FPS and render text
        fps = clock.get_fps()
        pygame.display.set_caption('Cube Demo FPS: {:.2f}'.format(fps))

        pygame.display.flip()
        clock.tick(60)

main()
