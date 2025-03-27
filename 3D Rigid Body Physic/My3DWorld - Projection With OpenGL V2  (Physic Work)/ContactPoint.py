import numpy as np

#MyCode
from Cube import Cube

class ContactPoint:
    def __init__(self, CubeA, CubeB, normal , x):
        self.CubeA = CubeA  # Position of the contact point on CubeA
        self.CubeB = CubeB  # Position of the contact point on CubeB

        self.AInverseBodyInertiaTensor = CubeA.getInverseBodyInertiaTensor()
        self.BInverseBodyInertiaTensor = CubeB.getInverseBodyInertiaTensor()

        self.normal = normal.copy()
        self.x = x.copy()  # Normal vector of the contact point
        
    def __str__(self):
        return f"Contact Point: \nCubeA Position: {self.cube_a_position}\nCubeB Position: {self.cube_b_position}\nNormal Vector: {self.normal_vector}\nPenetration Depth: {self.penetration_depth}"


def getPlaneContactPoint(CubeA,CubeB,collideNormal) :
    vertex_data_return = []
    for normal, normalpers in zip(CubeA.getAxes(), [CubeA.rightper, CubeA.upper, CubeA.forwardper]):
        # Positive
        a_dist_max = np.max(np.dot(CubeA.getTransformVertices(),normal))
        for pointB in CubeB.getTransformVertices():
            if abs(a_dist_max - np.dot(normal, pointB)) < 0.00001:
                for i, normalper in enumerate(normalpers):
                    dot = np.dot(CubeA.getTransformVertices(),normalper)
                    min_val = np.min(dot)
                    max_val = np.max(dot)
                    if not (min_val <= np.dot(normalper, pointB) <= max_val):
                        break
                    if i == 1:
                        vertex_data_return.append(ContactPoint(CubeA,CubeB,collideNormal,pointB))
    
    for normal, normalpers in zip(CubeA.getAxes(), [CubeA.rightper, CubeA.upper, CubeA.forwardper]):
        # Negative
        normal = normal.copy()*-1
        a_dist_max = np.max(np.dot(CubeA.getTransformVertices(),normal))
        for pointB in CubeB.getTransformVertices():
            if abs(a_dist_max - np.dot(normal, pointB)) < 0.00001:
                for i, normalper in enumerate(normalpers):
                    dot = np.dot(CubeA.getTransformVertices(),normalper)
                    min_val = np.min(dot)
                    max_val = np.max(dot)
                    if not (min_val <= np.dot(normalper, pointB) <= max_val):
                        break
                    if i == 1:
                        vertex_data_return.append(ContactPoint(CubeA,CubeB,collideNormal,pointB))

    temp = CubeB
    CubeB = CubeA
    CubeA = temp
    for normal, normalpers in zip(CubeA.getAxes(), [CubeA.rightper, CubeA.upper, CubeA.forwardper]):
        # Positive
        a_dist_max = np.max(np.dot(CubeA.getTransformVertices(),normal))
        for pointB in CubeB.getTransformVertices():
            if abs(a_dist_max - np.dot(normal, pointB)) < 0.00001:
                for i, normalper in enumerate(normalpers):
                    dot = np.dot(CubeA.getTransformVertices(),normalper)
                    min_val = np.min(dot)
                    max_val = np.max(dot)
                    if not (min_val <= np.dot(normalper, pointB) <= max_val):
                        break
                    if i == 1:
                        vertex_data_return.append(ContactPoint(CubeB,CubeA,collideNormal,pointB))

    for normal, normalpers in zip(CubeA.getAxes(), [CubeA.rightper, CubeA.upper, CubeA.forwardper]):
        # Negative
        normal = normal.copy()*-1
        a_dist_max = np.max(np.dot(CubeA.getTransformVertices(),normal))
        for pointB in CubeB.getTransformVertices():
            if abs(a_dist_max - np.dot(normal, pointB)) < 0.00001:
                for i, normalper in enumerate(normalpers):
                    dot = np.dot(CubeA.getTransformVertices(),normalper)
                    min_val = np.min(dot)
                    max_val = np.max(dot)
                    if not (min_val <= np.dot(normalper, pointB) <= max_val):
                        break
                    if i == 1:
                        vertex_data_return.append(ContactPoint(CubeB,CubeA,collideNormal,pointB))

    return vertex_data_return

def getEdgeContactPoint(line1, line2 , errortol=1e-3):
    # Extract points and direction vectors from the input lines
    p1, p2 = line1
    p3, p4 = line2
    direction1 = p2 - p1
    direction2 = p4 - p3

    # Check if the lines are parallel
    cross_product = np.cross(direction1, direction2)
    if np.allclose(cross_product, [0, 0, 0]):
        return None  # Lines are parallel

    # Solve the system of equations
    A = np.vstack((direction1, -direction2)).T
    b = p3 - p1
    t, s = np.linalg.lstsq(A, b, rcond=None)[0]
    # Calculate the intersection point
    intersection_point1 = p1 + t * direction1
    intersection_point2 = p3 + s * direction2

    if -0.00001 <= t <= 1.00001 and -0.00001 <= s <= 1.00001 and np.allclose(intersection_point1,intersection_point2 , atol=errortol):
      #print("Intersection Point Line 1 : " ,intersection_point1 , " :" , t , "Intersection Point Line 2 : " , intersection_point2, " :" , t )
      return intersection_point1
    return None