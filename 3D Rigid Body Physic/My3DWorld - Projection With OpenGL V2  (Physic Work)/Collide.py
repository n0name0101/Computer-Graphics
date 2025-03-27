from Cube import Cube 
import numpy as np
import copy

def Collide(CubeA , CubeB) : 
    AAxes = CubeA.getAxes()
    BAxes = CubeB.getAxes()
    edgeAB = [0,0]
    allAxes = AAxes + BAxes + [
        np.cross(AAxes[0],BAxes[0]) ,
        np.cross(AAxes[0],BAxes[1]) ,
        np.cross(AAxes[0],BAxes[2]) ,
        np.cross(AAxes[1],BAxes[0]) ,
        np.cross(AAxes[1],BAxes[1]) ,
        np.cross(AAxes[1],BAxes[2]) ,
        np.cross(AAxes[2],BAxes[0]) ,
        np.cross(AAxes[2],BAxes[1]) ,
        np.cross(AAxes[2],BAxes[2]) 
    ]
    allAxes = [axes/np.linalg.norm(axes) if not np.all(axes == 0) else axes for axes in allAxes]

    minOverlap = float('inf')
    collideAxis = None
    for axes in allAxes :
        if np.all(axes == 0) :
            continue
        b_proj_min = float('inf')
        a_proj_min = float('inf')
        b_proj_max = -float('inf')
        a_proj_max = -float('inf')
        iAmax = []
        iAmin = []
        iBmax = []
        iBmin = []
        for i,point in enumerate(CubeA.getTransformVertices()) :
            val = findScalarProjection(point,axes)
            if val > a_proj_max :
                a_proj_max = val
                iAmax = []
                iAmax.append(i)
            elif val == a_proj_max :
                iAmax.append(i)

            if val < a_proj_min :
                a_proj_min = val
                iAmin = []
                iAmin.append(i)
            elif val == a_proj_min :
                iAmin.append(i)

        for i,point in enumerate(CubeB.getTransformVertices()) :
            val = findScalarProjection(point,axes)
            if val > b_proj_max :
                b_proj_max = val
                iBmax = []
                iBmax.append(i)
            elif val == b_proj_max :
                iBmax.append(i)

            if val < b_proj_min :
                b_proj_min = val
                iBmin = []
                iBmin.append(i)
            elif val == b_proj_min :
                iBmin.append(i)

        overlap = findOverlap(a_proj_min,a_proj_max,b_proj_min,b_proj_max)
        if overlap < minOverlap :
            minOverlap = overlap
            collideAxis = axes
            if len(iAmax) == 4  and len(iBmax) == 4:
                edgeAB = (iAmax + iAmin , iBmax + iBmin)
            else :
                edgeAB = (iAmin[0:1]+iAmax[0:1], iBmin[0:1]+iBmax[0:1])
            #Save Axes
        if overlap <= 0 :
            return False , edgeAB , None #No Collide
    #print('Before : ',minOverlap)

    #Checking
    b_proj_min = float('inf')
    a_proj_min = float('inf')
    b_proj_max = -float('inf')
    a_proj_max = -float('inf')
    CubeACopy = copy.copy(CubeA)
    CubeACopy.x = CubeACopy.x + (minOverlap)*collideAxis
    for point in CubeACopy.getTransformVertices() :
        val = findScalarProjection(point,collideAxis)
        a_proj_max = val if val > a_proj_max else a_proj_max
        a_proj_min = val if val < a_proj_min else a_proj_min
    for point in CubeB.getTransformVertices() :
        val = findScalarProjection(point,collideAxis)
        b_proj_max = val if val > b_proj_max else b_proj_max
        b_proj_min = val if val < b_proj_min else b_proj_min
    #print("Overlap Checking : " , abs(findOverlap(a_proj_min,a_proj_max,b_proj_min,b_proj_max)))
    if abs(findOverlap(a_proj_min,a_proj_max,b_proj_min,b_proj_max)) >= 0.00001 :
        collideAxis = collideAxis*-1
        b_proj_min = float('inf')
        a_proj_min = float('inf')
        b_proj_max = -float('inf')
        a_proj_max = -float('inf')
        CubeACopy = copy.copy(CubeA)
        CubeACopy.x = CubeACopy.x + (minOverlap)*collideAxis
        for point in CubeACopy.getTransformVertices() :
            val = findScalarProjection(point,collideAxis)
            a_proj_max = val if val > a_proj_max else a_proj_max
            a_proj_min = val if val < a_proj_min else a_proj_min
        for point in CubeB.getTransformVertices() :
            val = findScalarProjection(point,collideAxis)
            b_proj_max = val if val > b_proj_max else b_proj_max
            b_proj_min = val if val < b_proj_min else b_proj_min
        #print("After : ", abs(findOverlap(a_proj_min,a_proj_max,b_proj_min,b_proj_max)) , '\n')

    #Update Cube 
    if CubeA.physic and CubeB.physic  :
        CubeA.x = CubeA.x + (minOverlap*0.5)*collideAxis
        CubeB.x = CubeB.x - (minOverlap*0.5)*collideAxis
    elif CubeA.physic: 
        CubeA.x = CubeA.x + (minOverlap)*collideAxis
    elif CubeB.physic: 
        CubeB.x = CubeB.x - (minOverlap)*collideAxis

    CubeA.addForce(CubeA.v * -1  * CubeA.mass)
    CubeA.addTorque(CubeA.L * -1)

    CubeB.addForce(CubeB.v * -1 * CubeB.mass)
    CubeB.addTorque(CubeB.L * -1)

    return True , edgeAB , collideAxis

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