import pygame
import random
import sys
from utils import *
import numpy as np
from math import sin, cos

class Cube:
    def __init__(self, SCREEN_SIZE=(1280,720) , physic=True ,mass=20,size=(100,100), pos=np.array([0, 0, 0]), I_body=20, I_body_inv=20, x=np.array([0, 0, 0]), P=None):
        self.SCREEN_WIDTH = SCREEN_SIZE[0]
        self.SCREEN_HEIGHT = SCREEN_SIZE[1]
        self.physic = physic
        self.size = size

        def GenerateReasonableRandomReal() :
            return 50 + 20 + random.uniform(0,1)
            
        dX2 = GenerateReasonableRandomReal()
        dY2 = GenerateReasonableRandomReal()
        dZ2 = GenerateReasonableRandomReal()

        if not physic :
            self.vertices = [
                np.array([-self.size[0] / 2, -self.size[1] / 2, self.size[1] / 2]),
                np.array([ self.size[0] / 2, -self.size[1] / 2, self.size[1] / 2]),
                np.array([ self.size[0] / 2,  self.size[1] / 2, self.size[1] / 2]),
                np.array([-self.size[0] / 2,  self.size[1] / 2, self.size[1] / 2]),
                np.array([-self.size[0] / 2,  self.size[1] / 2,-self.size[1] / 2]),
                np.array([-self.size[0] / 2, -self.size[1] / 2,-self.size[1] / 2]),
                np.array([ self.size[0] / 2, -self.size[1] / 2,-self.size[1] / 2]),
                np.array([ self.size[0] / 2,  self.size[1] / 2,-self.size[1] / 2]),
            ]
        else :
            self.vertices = [
                np.array([-dX2,-dY2, dZ2]),
                np.array([ dX2,-dY2, dZ2]),
                np.array([ dX2, dY2, dZ2]),
                np.array([-dX2, dY2, dZ2]),
                np.array([-dX2, dY2,-dZ2]),
                np.array([-dX2,-dY2,-dZ2]),
                np.array([ dX2,-dY2,-dZ2]),
                np.array([ dX2, dY2,-dZ2]),
            ]

        self.TransVertices = self.vertices
        self.faces = [
            (0,2,3) , (0,1,2) , # Depan
            (1,7,2) , (1,6,7) , #Belakang
            (6,5,4) , (4,7,6) ,
            (3,4,5) , (3,5,0) ,
            (3,7,4) , (3,2,7) ,
            (0,6,1) , (0,5,6) ,
        ]

        self.tex_coord = [[0,0] , [1,0] , [1,1] , [0,1]]
        self.tex_coord_indices = [
            [0,2,3] , [0,1,2] ,
            [0,2,3] , [0,1,2] ,
            [0,1,2] , [2,3,0] ,
            [2,3,0] , [2,0,1] ,
            [0,2,3] , [0,1,2] ,
            [3,1,2] , [3,0,1]
        ]

        self.edge_indices = [
            [0,1],[5,0],
            [5,6],[6,1],
            [1,2],[7,2],
            [6,7],[2,3],
            [7,4],[4,3],
            [3,0],[4,5],
        ]

        self.mass = (50.0)*0.4*dX2*dY2*dZ2
        # # Constant quantities
        self.oneovermass = 1/self.mass
        self.I_body = I_body
        self.I_inv = np.array([[3.0/(self.mass*(dY2*dY2 + dZ2*dZ2)), 0, 0],
                            [0, 3.0/(self.mass*(dX2*dX2 + dZ2*dZ2)), 0],
                            [0, 0, 3.0/(self.mass*(dX2*dX2 + dY2*dY2))]])  # Placeholder for inverse of I_body
        
        # self.mass = 300
        # self.inertia_tensor = (1/6) * self.mass * np.identity(3)
        # self.oneovermass = 1/mass
        # self.I_inv = np.linalg.inv(self.inertia_tensor)

        # State variables
        self.x = x  # Position vector
        self.R = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]])  # Rotation matrix

        # Linear momentum
        self.P = P

        # Angular momentum
        self.L = np.array([0,0,0])

        self.v = np.array([0,0,0])       # Placeholder for velocity
        self.angularVel = np.array([0,0,0])   # Placeholder for angular velocity

        # Computed quantities
        self.force = np.array([0,0,0])   # Placeholder for force
        self.torque = np.array([0,0,0])   # Placeholder for torque

        #Cube Axes
        vertices = np.dot(self.R, np.array(self.vertices).T).T
        self.forward , self.forwardper = self.triangle_orientation(self.faces[0],vertices)
        self.up , self.upper = self.triangle_orientation(self.faces[8],vertices)
        self.right , self.rightper = self.triangle_orientation(self.faces[2],vertices)

    def getAxes(self) :
        return [self.right , self.up , self.forward]

    def triangle_orientation(self,index,vertices):
        p1 = np.array(vertices[index[0]])
        
        # Calculate edges
        edge1 = np.array(vertices[index[1]]) - p1
        edge2 = np.array(vertices[index[2]]) - p1
        # return cross product
        orientation = np.cross(edge1, edge2)
        return orientation/np.linalg.norm(orientation) , [edge2/np.linalg.norm(edge2) , (vertices[index[1]]-vertices[index[2]])/np.linalg.norm((vertices[index[1]]-vertices[index[2]]))]
    
    def getTransformVertices(self) :
        return [i+self.x for i in self.TransVertices]
    
    def getTransformEdge(self) :
        return [[self.TransVertices[i]+self.x, self.TransVertices[j]+self.x] for i, j in self.edge_indices]
    
    def getTransformEdgebyTarget(self , target_values) :
        target_edge_indeces = [edge for edge in self.edge_indices if any(val in edge for val in target_values)]
        return [[self.TransVertices[i]+self.x, self.TransVertices[j]+self.x] for i, j in target_edge_indeces]

    def addForce(self,force) :
        self.force = self.force+ force

    def addTorque(self,torque) :
        self.torque = self.torque + torque

    def getInverseBodyInertiaTensor(self):
        return np.dot(np.dot(self.R,self.I_inv),self.R.T)
    
    def getRotationalVelocity(self,r) :
        return self.v + (np.cross(self.angularVel , r))

    def step(self, dt):        #Integrate
        if self.physic :
            #Add Gravity
            self.addForce(np.array((0,-981,0))*self.mass)   # 981cm = 9.81m

            #Update Position & Rotation Matrix
            self.x = self.x + dt*self.v
            self.R = integrateR_ME(self.R, self.angularVel, dt)
           
            #Update Velocity & Angular Momentum
            self.v = self.v + dt*(self.force*self.oneovermass)
            self.L = self.L + (dt * self.torque)

            self.angularVel = np.dot(self.getInverseBodyInertiaTensor(),self.L)

            #Update Axes and TransVertices
            self.TransVertices = np.dot(self.R, np.array(self.vertices).T).T
            self.forward , self.forwardper = self.triangle_orientation(self.faces[0],self.TransVertices)
            self.up , self.upper = self.triangle_orientation(self.faces[8],self.TransVertices)
            self.right , self.rightper = self.triangle_orientation(self.faces[2],self.TransVertices)
            
            #Reset Force and Torque
            self.force =  np.array((0, 0, 0))
            self.torque = np.array((0, 0, 0))

    def getTriangle(self, camera_position):
        returnPointList = []
        returnTextureList = []
        # Calculate distances of faces from the camera
        face_distances = []

        for index,face in enumerate(self.faces):
            #triangleOrientation = np.dot(self.R,self.triangle_orientation(face,self.vertices))
            triangleOrientation ,triangleOrientationper = self.triangle_orientation(face,self.TransVertices)
            # Project and draw each face
            if np.dot(triangleOrientation,camera_position-self.x) > 0 :
                points = [self.TransVertices[vertex] + self.x for vertex in face]
                texture = [self.tex_coord[i] for i in self.tex_coord_indices[index]]
                returnPointList.append(points)
                returnTextureList.append(texture)
        return zip(returnPointList , returnTextureList)
    
    def getTexCoor(self):
        print([self.tex_coord[ind] for triangle in self.tex_coord_indices for ind in triangle] , '\n')
