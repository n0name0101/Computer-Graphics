import numpy as np
import pygame
import multiprocessing
import itertools
import glm 
import moderngl
import threading

from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from queue import Queue

#MyCode
from Camera import Camera
from Collide import *
from ContactPoint import *

class World3D:
    def __init__(self, SCREEN_SIZE=(1280, 720) , camera=np.array([0,0,-1000]) , lookat=np.array([0,0,1])):
        self.SCREEN_WIDTH = SCREEN_SIZE[0]
        self.SCREEN_HEIGHT = SCREEN_SIZE[1]
        self.camera = Camera(pos=camera,lookat=lookat)
        self.cubes = []
        self.controlcube = 0

    def add_cube(self, cube):
        self.cubes.append(cube)

    def drawOpenGLOptimize(self , ctx , shader_program , texture) :
        #Load Texture
        texture.use()

        vertex_data = []
        texture_data = []
        for cube in self.cubes:
            COLOR = RED
            if not len(self.cubes) == 0 and self.cubes[self.controlcube] is cube:
                COLOR = GREEN
            for points , textures in cube.getTriangle(self.camera.pos):
                for point , texture in zip(points,textures):
                    # Apply View Matrix to Convert to World
                    point = np.dot(np.append(point, 1), self.camera.get_view_matrix())[:-1]
                    # Invert Z-axis to match OpenGL's coordinate system
                    point[2] *= -1
                    vertex_data.append(point.tolist())
                    texture_data.append(texture)
        vertex_data = np.array(vertex_data,dtype='f4')
        texture_data = np.array(texture_data,dtype='f4')

        vertex_data = np.hstack([texture_data,vertex_data])
        #print(vertex_data , '\n')
        vbo = ctx.buffer(vertex_data)
        vao = ctx.vertex_array(shader_program,[(vbo,'2f 3f', 'in_texcoord_0' , 'in_position')])
        vao.render()
        vbo.release()
        vao.release()

    def camera_lookat_rotation(self, dx, dy):
        # Rotation speed
        rotation_speed = 0.01

        # Get current camera position and lookat vector
        pos = self.camera.pos
        lookat = self.camera.lookat

        # Calculate rotation around up and right vectors
        up = np.array([0, 1, 0])
        right = np.cross(lookat, up)
        rotation_up = rotation_speed * dx * right
        rotation_right = rotation_speed * dy * up

        # Update lookat vector
        lookat = rotate_vector(lookat, rotation_up)
        lookat = rotate_vector(lookat, rotation_right)
        # Update camera lookat vector
        self.camera.lookat = lookat

    def step(self, dt , ctx , shader_program):
        contactpoints = []
        for CubeA , CubeB  in itertools.combinations(self.cubes, 2) :
            coll , edgeAB , collideNormal = Collide(CubeA , CubeB)
            if coll :
                temp = getPlaneContactPoint(CubeA,CubeB,collideNormal)
                contactpoints += temp
                if (len(temp) < 4) and collideNormal is not None :
                    #print(edgeAB , '\n')
                    for lineA in CubeA.getTransformEdgebyTarget(edgeAB[0]) :
                        for lineB in CubeB.getTransformEdgebyTarget(edgeAB[1]) :
                            temp = getEdgeContactPoint(lineA,lineB,errortol=1e-5)
                            if (temp) is not None :
                                contactpoints.append(ContactPoint(CubeA,CubeB,collideNormal,temp))

        # Draw Contact Point
        # vertex_data = []
        # if len(contactpoints) != 0 :
        #     glDisable(GL_DEPTH_TEST)
        #     glPointSize(5.0)
        #     for contactpoint in contactpoints:
        #         # Apply View Matrix to Convert to World
        #         point = np.dot(np.append(contactpoint.x.copy(), 1), self.camera.get_view_matrix())[:-1]
        #         # Invert Z-axis to match OpenGL's coordinate system
        #         point[2] *= -1
        #         vertex_data.append(point.tolist())
        #     vertex_data = np.array(vertex_data,dtype='f4')
        #     #print(vertex_data , '\n')
        #     vbo = ctx.buffer(vertex_data)
        #     vao = ctx.vertex_array(shader_program,[(vbo,'3f', 'in_position')])
        #     vao.render(moderngl.POINTS)
        #     vbo.release()
        #     vao.release()
        #     glEnable(GL_DEPTH_TEST)

        #Integrate All Bodies
        for cube in self.cubes:
            cube.step(dt)

        # print("Velocity Before : [ X : " , self.cubes[0].v[0] , " , Y : " , self.cubes[0].v[1] , " , Z : " , self.cubes[0].v[2] , " ]")
        # print("L Before : [ X : " , self.cubes[0].L[0] , " , Y : " , self.cubes[0].L[1] , " , Z : " , self.cubes[0].L[2] , " ]")
        CubeAGroundAddForce = True
        for contactpoint in contactpoints :
            RESOLVE_LIMIT = 50
            CubeA = contactpoint.CubeA
            CubeB = contactpoint.CubeB

            if CubeA.physic and CubeB.physic :
                CollideNormal1 = contactpoint.normal
                RA = contactpoint.x - CubeA.x
                RB = contactpoint.x - CubeB.x
                Counter = 0
                vr = np.dot(CollideNormal1,(CubeA.getRotationalVelocity(RA) - CubeB.getRotationalVelocity(RB)))

                jatas = -(1.0+1.0)*vr
                a = np.dot(contactpoint.AInverseBodyInertiaTensor,np.cross(RA,CollideNormal1))
                b = np.dot(contactpoint.BInverseBodyInertiaTensor,np.cross(RB,CollideNormal1))
                jbawah = CubeA.oneovermass + CubeB.oneovermass + \
                        np.dot(CollideNormal1,np.cross(a,RA)+np.cross(b,RB))
                j = (jatas/jbawah)

                CubeA.v = (CubeA.v) + 0.8*(j*CollideNormal1*(CubeA.oneovermass))
                CubeA.L = (CubeA.L) + 0.8*(np.cross(RA,j*CollideNormal1))
                CubeA.angularVel = np.dot(contactpoint.AInverseBodyInertiaTensor,CubeA.L)

                CubeB.v = (CubeB.v) - 0.8*(j*CollideNormal1*(CubeB.oneovermass))
                CubeB.L = (CubeB.L) - 0.8*(np.cross(RB,j*CollideNormal1))
                CubeB.angularVel = np.dot(contactpoint.BInverseBodyInertiaTensor,CubeB.L)

            # CubeA
            elif CubeA.physic :
                CollideNormal1 = contactpoint.normal
                R = contactpoint.x - CubeA.x
                Counter = 0
                while np.dot(CollideNormal1,CubeA.getRotationalVelocity(R)) < 0.0 :
                    vr = np.dot(CollideNormal1,(CubeA.getRotationalVelocity(R)))
                    jatas = -(1.0+1.0)*vr
                    a = np.dot(contactpoint.AInverseBodyInertiaTensor,np.cross(R,CollideNormal1))
                    jbawah = CubeA.oneovermass + np.dot(np.cross(a,R) , CollideNormal1)
                    j = (jatas/jbawah)

                    CubeA.v = (CubeA.v) + 0.6*(j*CollideNormal1*(CubeA.oneovermass))
                    CubeA.L = (CubeA.L) + 0.6*(np.cross(R,j*CollideNormal1))
                    CubeA.angularVel = np.dot(contactpoint.AInverseBodyInertiaTensor,CubeA.L)
                    Counter = Counter+1
                    if Counter == RESOLVE_LIMIT :
                        #Eliminate The Gravity
                        if np.dot(CubeA.v , CollideNormal1) < 0.0 :
                            CubeA.v = CubeA.v - CollideNormal1 * np.dot(CubeA.v , CollideNormal1)
                        break
                #Eliminate The Gravity
                if np.dot(CubeA.v , CollideNormal1) < 0.0 :
                    CubeA.v = CubeA.v - CollideNormal1 * np.dot(CubeA.v , CollideNormal1)

            # CubeB
            elif CubeB.physic :
                CollideNormal1 = -contactpoint.normal
                R = contactpoint.x - CubeB.x
                Counter = 0
                while np.dot(CollideNormal1,CubeB.getRotationalVelocity(R)) < 0.0 :
                    vr = np.dot(CollideNormal1,(CubeB.getRotationalVelocity(R)))
                    jatas = -(1.0+1.0)*vr
                    a = np.dot(contactpoint.BInverseBodyInertiaTensor,np.cross(R,CollideNormal1))
                    jbawah = CubeB.oneovermass + np.dot(np.cross(a,R) , CollideNormal1)
                    j = (jatas/jbawah)

                    CubeB.v = (CubeB.v) + 0.6*(j*CollideNormal1*(CubeB.oneovermass))
                    CubeB.L = (CubeB.L) + 0.6*(np.cross(R,j*CollideNormal1))
                    CubeB.angularVel = np.dot(contactpoint.BInverseBodyInertiaTensor,CubeB.L)
                    Counter = Counter+1
                    if Counter == RESOLVE_LIMIT :
                        #Eliminate The Gravity
                        if np.dot(CubeB.v , CollideNormal1) < 0.0 :
                            CubeB.v = CubeB.v - CollideNormal1 * np.dot(CubeB.v , CollideNormal1)
                        break
                #Eliminate The Gravity
                if np.dot(CubeB.v , CollideNormal1) < 0.0 :
                    CubeB.v = CubeB.v - CollideNormal1 * np.dot(CubeB.v , CollideNormal1)

        # print("Velocity After : [ X :", self.cubes[0].v[0], ", Y :", self.cubes[0].v[1], ", Z :", self.cubes[0].v[2], "]")
        # print("L After : [ X :", self.cubes[0].L[0], ", Y :", self.cubes[0].L[1], ", Z :", self.cubes[0].L[2], "]")
        # print("-------------------------------------------------------------------------------------------")

def rotate_vector(vector, rotation):
    # Construct rotation matrices
    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(rotation[0]), -np.sin(rotation[0])],
                           [0, np.sin(rotation[0]), np.cos(rotation[0])]])
    rotation_y = np.array([[np.cos(rotation[1]), 0, np.sin(rotation[1])],
                           [0, 1, 0],
                           [-np.sin(rotation[1]), 0, np.cos(rotation[1])]])
    rotation_z = np.array([[np.cos(rotation[2]), -np.sin(rotation[2]), 0],
                           [np.sin(rotation[2]), np.cos(rotation[2]), 0],
                           [0, 0, 1]])

    # Apply rotations
    vector = np.dot(rotation_x, vector)
    vector = np.dot(rotation_y, vector)
    vector = np.dot(rotation_z, vector)

    return vector

def get_shader_program(shader_name , ctx) :
    with open(f'Shaders/{shader_name}.vert') as file :
        vertex_shader = file.read()
    with open(f'Shaders/{shader_name}.frag') as file :
        fragment_shader = file.read()
    program = ctx.program(vertex_shader=vertex_shader,fragment_shader=fragment_shader)
    return program