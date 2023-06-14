import math
import numpy as np

def twoDToPyGame(twoD , pyObject):
    screen_info = pyObject.display.Info()
    return (int(twoD[0] + screen_info.current_w/2.0),int(screen_info.current_h/2.0 - twoD[1]))

def threeTotwo(threeD):
    return (threeD[0], threeD[1])

def perspectiveProjection(threeD,pyObject,fovy=math.radians(60), aspect=1, near=5, far=3000):
    f = 1.0 / math.tan(fovy / 2)
    nf = 1.0 / (near - far)

    perspectiveMatrix =  [
        [f*aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (-near-far) * nf, (2*far*near) * nf],
        [0, 0, 1 , 0]
    ]

    # Append 1 to the `threeD` array and convert it to a NumPy array
    perspectiveInput = np.append(threeD, 1)
    perspectiveInput = np.array(perspectiveInput)

    # Perform matrix multiplication
    output = np.dot(perspectiveMatrix, perspectiveInput)

    screen_info = pyObject.display.Info()
    x = output[0]/output[3]
    y = output[1]/output[3]
    z = output[2]/output[3]

    if z > 1.0 or z < -1.0 :
        return 0
    return [int(screen_info.current_w*(float(x+1)/2.0)),int(screen_info.current_h-(float(y+1)/2.0)*screen_info.current_h),z]

def getViewMat(_camPosVec,_lookAtVec,_upVec):
    #print('--------------------------------------------------')
    #print('Cam Pos :',_camPosVec)
    #print('Look At :',_lookAtVec)
    #print('Up Pos  :',_upVec)
    #print('--------------------------------------------------')
    _lookAtVec = _lookAtVec-_camPosVec
    newFo = _lookAtVec.normalize()

    #a = newFo * (_upVec * newFo)
    #newUp = (_upVec-a).normalize()

    #newRi = newUp.cross(newFo).normalize()

    #Implement With the method that i read in arthiche 'learnopengl - camera'
    newRi = _upVec.cross(newFo).normalize()
    newUp = newFo.cross(newRi)

    perspectiveMatrix = np.dot(
        np.array([
        [newRi.x, newRi.y, newRi.z, 0],
        [newUp.x, newUp.y, newUp.z, 0],
        [newFo.x, newFo.y, newFo.z, 0],
        [0, 0, 0, 1]
        ])
        ,np.array([
        [1, 0, 0, -_camPosVec.x],
        [0, 1, 0, -_camPosVec.y],
        [0, 0, 1, -_camPosVec.z],
        [0, 0, 0, 1]
        ]))
    return perspectiveMatrix

def mulView(_persMat,_input):
    _input[0].append(1)
    _input[1].append(1)
    _input[2].append(1)
    inputMat = np.array(_input).transpose()
    inputMat = np.dot(_persMat, inputMat)
    _input = inputMat.transpose().tolist()
    _input[0].pop(3)
    _input[1].pop(3)
    _input[2].pop(3)

    #output = np.dot(_persMat, inputMat)
    return _input

def perspectiveClipZ(data):
    returnlist = []
    for vertex in data :
        if(vertex == 0) :
            continue
        returnlist.append([vertex[0],vertex[1],vertex[2]])
    return returnlist

def perspectiveSort(data):
    color = []

    def sortingRule(n) :
        return ((n[0][2]+1) + (n[1][2]+1) + (n[2][2]+1) ) / 3
    data.sort(key=sortingRule,reverse=True)
    for triangle in data :
        color.append(triangle.pop(3))
        for vertex in triangle :
            vertex.pop(2)
    return data,color
