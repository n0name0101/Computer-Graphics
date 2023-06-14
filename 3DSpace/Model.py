import pygame
import numpy as np

from Vector2 import *
from Vector3 import *
from Triangle import *
from GeneralProjection import *

class Model:
    def __init__(self, size, position , angle_x=0 , angle_y=0 , angle_z=0):
        self.size = size
        self.position = position

        #Rotation Angle
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.vertices = [
            Vector3(- self.size / 2, + self.size / 2, + self.size / 2), # Left Atas
            Vector3(+ self.size / 2, + self.size / 2, + self.size / 2), # Right Atas
            Vector3(- self.size / 2, - self.size / 2, + self.size / 2), # Left Bawah
            Vector3(+ self.size / 2, - self.size / 2, + self.size / 2), # Right Bawah
            Vector3(- self.size / 2, + self.size / 2, - self.size / 2),
            Vector3(+ self.size / 2, + self.size / 2, - self.size / 2),
            Vector3(- self.size / 2, - self.size / 2, - self.size / 2),
            Vector3(+ self.size / 2, - self.size / 2, - self.size / 2),
        ]
        self.triangles = [
            (2, 0, 1), (2, 1, 3),  # Front face
            (7, 5, 4), (7, 4, 6),  # Back face
            (6, 4, 0), (6, 0, 2),  # Left face
            (3, 1, 5), (3, 5, 7),  # Right face
            (0, 4, 5), (0, 5, 1),  # Top face
            (6, 2, 3), (6, 3, 7),  # Bottom face
        ]

    # Getter and Setter for angle_x
    def setangle_x(self, value):
        self.angle_x = value

    def setangle_y(self, value):
        self.angle_y = value

    def setangle_z(self, value):
        self.angle_z = value

    #3D Transformation
    #Rotation
    def rotate(self, angle_x=0, angle_y=0, angle_z=0):
        rotation_matrix_x = np.array([[1, 0, 0],
                                      [0, np.cos(angle_x), -np.sin(angle_x)],
                                      [0, np.sin(angle_x), np.cos(angle_x)]])

        rotation_matrix_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                                      [0, 1, 0],
                                      [-np.sin(angle_y), 0, np.cos(angle_y)]])

        rotation_matrix_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                                      [np.sin(angle_z), np.cos(angle_z), 0],
                                      [0, 0, 1]])

        rotation_matrix = np.dot(rotation_matrix_x, np.dot(rotation_matrix_y, rotation_matrix_z))

        # Apply rotation to each vertex
        vertices = [np.dot([vertex.x,vertex.y,vertex.z], rotation_matrix) for vertex in self.vertices]
        verticesVec = [Vector3(i[0],i[1],i[2]) for i in vertices]
        return verticesVec

    def draw(self, screen,res,camVec,lookAtVec,upVec):
        triangle2DCoordinates = []
        vertices = self.rotate(self.angle_x,self.angle_y,self.angle_z)

        #Create ViewMatrix
        viewMatrix = getViewMat(camVec,camVec+lookAtVec,upVec)

        color = [[255, 0, 0],[255, 0, 0],[0, 255, 255],[0, 255, 255],[255, 0, 255] ,[255, 0, 255] ,[255, 255, 0] ,[255, 255, 0] ,[0, 0, 255] ,[0, 0, 255] ,[0, 255, 0] ,[0, 255, 0] ]
        iCounter = 0
        printcolor = []
        for triangle in self.triangles:
            triangle3D = (vertices[triangle[0]], vertices[triangle[1]]
                          , vertices[triangle[2]])

            #Cross Product Checking
            firstVec =  (triangle3D[1] - triangle3D[0])
            secondVec = (triangle3D[2] - triangle3D[0])

            color1 = color[iCounter]
            iCounter += 1
            if((firstVec.cross(secondVec).normalize()*Vector3(0,0,1))  >= 0 or True):
                triangle3D = ((vertices[triangle[0]]+self.position).getlist()
                            , (vertices[triangle[1]]+self.position).getlist()
                            , (vertices[triangle[2]]+self.position).getlist())

                #3D to 2D Projection Orthagraphic
                #triangle2D = [threeTotwo(vertex) for vertex in triangle3D]
                #Convert 2D Cartesian Coordinate To PyGame Coordinate
                #triangle2D = [twoDToPyGame(vertex,res) for vertex in triangle2D]

                #ViewMatrix Multiplication

                triangle3D = mulView(viewMatrix,triangle3D)
                triangle2D = [perspectiveProjection(vertex,res,aspect=(res.display.Info().current_h/res.display.Info().current_w)) for vertex in triangle3D]
                triangle2D = perspectiveClipZ(triangle2D)
                if(len(triangle2D) == 3) :
                    #printcolor.append(color1)
                    triangle2D.append(color1)
                    triangle2DCoordinates.append(triangle2D)

        triangle2DCoordinates,printcolor = perspectiveSort(triangle2DCoordinates)
        iCounter = 0
        for triangle in triangle2DCoordinates:
            pygame.draw.polygon(screen, (0, 0, 255), triangle, 5)  # Draw outline
            pygame.draw.polygon(screen, printcolor[iCounter], triangle)
            #vlist = []
            #for i in triangle :
                #vlist.append(Vector2(i[0],i[1]))
            #drawTriangle(screen,vlist[1],vlist[0],vlist[2])
            iCounter = iCounter + 1
            #pygame.draw.circle(screen, (255,255,255), triangle[0] , 5)
            #pygame.draw.circle(screen, (255,255,255), triangle[1] , 5)
            #pygame.draw.circle(screen, (255,255,255), triangle[2] , 5)
