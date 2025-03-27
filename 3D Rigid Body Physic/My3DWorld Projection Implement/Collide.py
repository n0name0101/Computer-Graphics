from Cube import Cube 
import numpy as np

def Collide(CubeA , CubeB) : 
    AAxes = CubeA.getAxes()
    BAxes = CubeB.getAxes()
    allAxes = AAxes + BAxes + [
        np.cross(AAxes[0],BAxes[0]),
        np.cross(AAxes[0],BAxes[1]),
        np.cross(AAxes[0],BAxes[2]),
        np.cross(AAxes[1],BAxes[0]),
        np.cross(AAxes[1],BAxes[1]),
        np.cross(AAxes[1],BAxes[2]),
        np.cross(AAxes[2],BAxes[0]),
        np.cross(AAxes[2],BAxes[1]),
        np.cross(AAxes[2],BAxes[2])
    ]

    minOverlap = float('inf')
    collideAxis = None
    for axes in allAxes :
        if np.all(axes == 0) :
            continue
        b_proj_min = float('inf')
        a_proj_min = float('inf')
        b_proj_max = -float('inf')
        a_proj_max = -float('inf')

        for point in CubeA.getTransformVertices() :
            val = findScalarProjection(point,axes)
            a_proj_max = val if val > a_proj_max else a_proj_max
            a_proj_min = val if val < a_proj_min else a_proj_min
        for point in CubeB.getTransformVertices() :
            val = findScalarProjection(point,axes)
            b_proj_max = val if val > b_proj_max else b_proj_max
            b_proj_min = val if val < b_proj_min else b_proj_min

        overlap = findOverlap(a_proj_min,a_proj_max,b_proj_min,b_proj_max)
        
        if overlap < minOverlap :
            minOverlap = overlap
            collideAxis = axes
            #Save Axes
        if overlap <= 0 :
            return #No Collide

    #Update Cube 
    if CubeA.physic and CubeB.physic  :
        CubeA.x = CubeA.x + (minOverlap/2)*collideAxis
        CubeB.x = CubeB.x - (minOverlap/2)*collideAxis
    elif CubeA.physic: 
        CubeA.x = CubeA.x + (minOverlap)*collideAxis
    elif CubeB.physic: 
        CubeB.x = CubeB.x - (minOverlap)*collideAxis
        
def findScalarProjection(point, axis) :
	return np.dot(point, axis)

def findOverlap(astart, aend, bstart, bend) :
    if astart < bstart :
        if aend < bstart :
            return 0.0
        return aend - bstart
    if bend < astart :
        return 0.0
    return bend - astart