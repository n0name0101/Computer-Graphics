import pygame
import sys
from utils import *
import numpy as np
from math import sin, cos

class Cube:
    def __init__(self, SCREEN_SIZE=(1280,720) , physic=True ,mass=20,size=(100,100), pos=np.array([0, 0, 0]), I_body=20, I_body_inv=20, x=np.array([0, 0, 0]), P=None, L=None):
        self.SCREEN_WIDTH = SCREEN_SIZE[0]
        self.SCREEN_HEIGHT = SCREEN_SIZE[1]
        self.physic = physic
        self.size = size
        self.vertices = [
            [-self.size[0] / 2, -self.size[1] / 2, - self.size[1] / 2],
            [self.size[0] / 2, -self.size[1] / 2, - self.size[1] / 2],
            [self.size[0] / 2, self.size[1] / 2, - self.size[1] / 2],
            [-self.size[0] / 2, self.size[1] / 2, - self.size[1] / 2],
            [-self.size[0] / 2, -self.size[1] / 2, self.size[1] / 2],
            [self.size[0] / 2, -self.size[1] / 2, self.size[1] / 2],
            [self.size[0] / 2, self.size[1] / 2, self.size[1] / 2],
            [-self.size[0] / 2, self.size[1] / 2, self.size[1] / 2]
        ]
        self.faces = [
            (2,1,0) , (2,0,3) , # Depan
            (5,6,7) , (5,7,4) , #Belakang
            (3,7,6) , (3,6,2) ,
            (0,4,7) , (0,7,3) ,
            (1,5,4) , (1,4,0) ,
            (2,6,5) , (2,5,1) ,
        ]

        # Constant quantities
        self.mass = mass
        self.I_body = I_body
        self.I_body_inv = I_body_inv

        # State variables
        self.x = x  # Position vector
        self.R = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]])  # Rotation matrix

        # Linear momentum
        self.P = P

        # Angular momentum
        self.L = L

        # Derived quantities
        self.I_inv = None  # Placeholder for inverse of I_body
        self.v = np.array([0,0,0])       # Placeholder for velocity
        self.omega = None   # Placeholder for angular velocity

        # Computed quantities
        self.force = None   # Placeholder for force
        self.torque = None  # Placeholder for torque

        #Cube Axes
        vertices = np.dot(self.R, np.array(self.vertices).T).T
        self.forward = self.triangle_orientation(self.faces[2],vertices)
        self.up = self.triangle_orientation(self.faces[4],vertices)
        self.right = self.triangle_orientation(self.faces[10],vertices)

    def getAxes(self) :
        return [self.forward , self.right , self.up]

    def triangle_orientation(self,index,vertices):
        p1 = np.array(vertices[index[0]])
        
        # Calculate edges
        edge1 = np.array(vertices[index[1]]) - p1
        edge2 = np.array(vertices[index[2]]) - p1

        # return cross product
        orientation = np.cross(edge1, edge2)
        return orientation/np.linalg.norm(orientation)

    def getTransformVertices(self) :
        return [i+self.x for i in np.dot(self.R, np.array(self.vertices).T).T]

    def step(self, dt , change):
        if self.physic :
            # Angular
            if change :
                self.omega = np.random.randint(-1000, 1000, size=3) #np.random.randint(-500, 500 + 1, size=3) #np.array((2, 2, 5))
            else :
                self.omega = np.array((0, 0, 0))
            self.R = update_rotation_matrix_exponential_coordinates(self.R, self.omega, dt)

            #Linear
            self.v = self.v + dt*np.array([0,-50,0])
            self.x = self.x + dt*self.v

            self.v = self.v - 0.1*self.v

            #Update Axes
            rotated_vertices = np.dot(self.R, np.array(self.vertices).T).T
            self.forward = self.triangle_orientation(self.faces[2],rotated_vertices)
            self.up = self.triangle_orientation(self.faces[4],rotated_vertices)
            self.right = self.triangle_orientation(self.faces[10],rotated_vertices)

    def getTriangle(self, surface , camera_position):
        returnPointList = []
        # Calculate distances of faces from the camera
        rotated_vertices = np.dot(self.R, np.array(self.vertices).T).T
        face_distances = []
        
        for face in self.faces:
            average_distance = np.sum([np.linalg.norm((rotated_vertices[vertex] + self.x) - camera_position) for vertex in face])
            face_distances.append((average_distance, face))
        # Sort faces based on distances (farthest to nearest)
        sorted_faces = sorted(face_distances, key=lambda x: x[0], reverse=True)

        for _, face in sorted_faces:
            #triangleOrientation = np.dot(self.R,self.triangle_orientation(face,self.vertices))
            triangleOrientation = self.triangle_orientation(face,rotated_vertices)
            
            # Project and draw each face
            if np.dot(triangleOrientation,camera_position-self.x) > 0 :
                points = [rotated_vertices[vertex] + self.x for vertex in face]
                returnPointList.append(points)
        
        return returnPointList