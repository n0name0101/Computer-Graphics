import numpy as np
import pygame
from utils import *
import itertools

#MyCode
from Camera import Camera
from Collide import *

class World3D:
    def __init__(self, SCREEN_SIZE=(1280, 720) , camera=np.array([0,0,-1000]) , lookat=np.array([0,0,1])):
        self.SCREEN_WIDTH = SCREEN_SIZE[0]
        self.SCREEN_HEIGHT = SCREEN_SIZE[1]
        self.camera = Camera(pos=camera,lookat=lookat)
        self.cubes = []
        self.controlcube = 0

    def add_cube(self, cube):
        self.cubes.append(cube)

    def draw(self, surface):
        focal_length = 1.0
        aspect_ratio = self.SCREEN_WIDTH / self.SCREEN_HEIGHT  # Assuming 16:9 aspect ratio
        near = 0.1
        far = 100.0
        allobject = []
        # Sort cubes 
        sorted_cubes = sorted(self.cubes, key=lambda cube: np.dot(cube.x - self.camera.pos, self.camera.lookat), reverse=True)
        sorted_cubes = sorted(self.cubes, key=lambda cube: np.linalg.norm(cube.x - self.camera.pos), reverse=True)
        #sorted_cubes = sorted(self.cubes, key=lambda cube: np.dot((cube.x - self.camera.pos), self.camera.lookat), reverse=True)

        for cube in sorted_cubes:
            COLOR = RED
            if not len(self.cubes) == 0 and self.cubes[self.controlcube] is cube :
                COLOR = GREEN
            if np.dot(cube.x - self.camera.pos , self.camera.lookat) > 0 :
                for points in cube.getTriangle(surface,self.camera.pos) :
                    # Applied View Matrix to Convert to World
                    points = [np.dot(np.append(point,1),self.camera.get_view_matrix() )[:-1] for point in points]

                    #print(" Triangle Point : " , points , "\n")
                    projected_points = [self.perspective_projection(point, focal_length, aspect_ratio, near, far) for point in points]
                    
                    # Check if all projected points are within the screen boundaries
                    if all(0 <= point[0] <= self.SCREEN_WIDTH and 0 <= point[1] <= self.SCREEN_HEIGHT for point in projected_points):
                        # Draw filled polygon (triangle)
                        pygame.draw.polygon(surface, COLOR, projected_points)

                        # Draw black edges
                        for i in range(len(projected_points)):
                            pygame.draw.line(surface, BLACK, projected_points[i], projected_points[(i + 1) % len(projected_points)], 1)

    def drawSorted(self, surface):
        focal_length = 1.0
        aspect_ratio = self.SCREEN_WIDTH / self.SCREEN_HEIGHT  # Assuming 16:9 aspect ratio
        near = 0.1
        far = 100.0
        allTriangles = []

        for cube in self.cubes:
            COLOR = RED
            if not len(self.cubes) == 0 and self.cubes[self.controlcube] is cube :
                COLOR = GREEN
            if np.dot(cube.x - self.camera.pos , self.camera.lookat) > 0 :
                for Triangle in cube.getTriangle(surface,self.camera.pos) :
                    allTriangles.append([Triangle , COLOR])
         # Define a sorting function based on the depth of the triangles
        def depth_sorting(triangle_data):
            points, _ = triangle_data
            return np.mean(np.array([ np.abs((point-self.camera.pos)[2]) for point in points]))

        # Sort all triangles based on depth
        allTriangles.sort(key=depth_sorting,reverse=True)

        for points , COLOR in allTriangles :
                # Applied View Matrix to Convert to World
                points = [np.dot(np.append(point,1),self.camera.get_view_matrix() )[:-1] for point in points]

                #print(" Triangle Point : " , points , "\n")
                projected_points = [self.perspective_projection(point, focal_length, aspect_ratio, near, far) for point in points]
                
                # Check if all projected points are within the screen boundaries
                if all(0 <= point[0] <= self.SCREEN_WIDTH and 0 <= point[1] <= self.SCREEN_HEIGHT for point in projected_points):
                    # Draw filled polygon (triangle)
                    pygame.draw.polygon(surface, COLOR, projected_points)

                    # Draw black edges
                    for i in range(len(projected_points)):
                        pygame.draw.line(surface, BLACK, projected_points[i], projected_points[(i + 1) % len(projected_points)], 1)

    def project(self, vert):
        # Calculate the vector from the camera position to the vertex
        direction = vert 
        
        # Orthogonal projection along the direction vector onto the xy plane
        projected_point = np.array([direction[0], direction[1]]) + np.array([self.SCREEN_WIDTH//2,self.SCREEN_HEIGHT//2])
        
        return projected_point

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

    def perspective_projection(self,point, focal_length, aspect_ratio, near, far):
        # Homogeneous coordinates (add 1 as the fourth component)
        point = np.array([point[0], point[1], point[2], 1])
        
        # Perspective projection matrix
        projection_matrix = np.array([
            [focal_length / aspect_ratio, 0, 0, 0],
            [0, focal_length, 0, 0],
            [0, 0, (far + near) / (far - near), -2 * far * near / (far - near)],
            [0, 0, 1, 0]
        ])
        # Apply projection
        projected_point = np.dot(projection_matrix, point)
        # Normalize homogeneous coordinates
        projected_point /= projected_point[3]

        # Return 2D projected point (discard fourth component)
        return self.map_to_screen(projected_point[:3],self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
    
    def map_to_screen(self,projected_point, screen_width, screen_height):
        # Scale the projected point to fit within the screen's boundaries
        scaled_point = np.array([
            projected_point[0] * (screen_width / 2),
            projected_point[1] * (screen_height / 2),
            projected_point[2]
        ])
        
        # Translate the scaled point to the center of the screen
        translated_point = np.array([
            scaled_point[0] + (screen_width / 2),
            screen_height - (scaled_point[1] + (screen_height / 2)),
            scaled_point[2]
        ])

        return np.array([translated_point[0],translated_point[1]])

    def step(self, dt, change):
        for CubeA , CubeB  in itertools.combinations(self.cubes, 2) :
            Collide(CubeA , CubeB)

        for cube in self.cubes:
            cube.step(dt, change)

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
