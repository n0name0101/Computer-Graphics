import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

size = 10

vertices = (
    [-size / 2, -size / 2, - size / 2],
    [size / 2, -size / 2, - size / 2],
    [size / 2, size / 2, - size / 2],
    [-size / 2, size / 2, - size / 2],
    [-size / 2, -size / 2, size / 2],
    [size / 2, -size / 2, size / 2],
    [size / 2, size / 2, size / 2],
    [-size / 2, size / 2, size / 2]
)

faces = [
    (2, 1, 0), (2, 0, 3),  # Front
    (5, 6, 7), (5, 7, 4),  # Back
    (3, 7, 6), (3, 6, 2),
    (0, 4, 7), (0, 7, 3),
    (1, 5, 4), (1, 4, 0),
    (2, 6, 5), (2, 5, 1),
]


def Cube():
    glPointSize(10.0)  # Set point size to 5.0 (adjust as needed)
    glBegin(GL_POINTS)
    glColor3fv([0, 1, 0])  # Set point color to white
    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()
    
    for i, face in enumerate(faces):
        # Draw edges
        glBegin(GL_LINE_LOOP)
        glColor3fv([1,1,1])
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()
        
        glBegin(GL_TRIANGLES)
        glColor3fv([1,0,0])
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()


def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(0.0, 0.0, -50)
    glLineWidth(2.0)         # Adjust Line Thickness
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glRotatef(1, 3, 1, 1)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()
