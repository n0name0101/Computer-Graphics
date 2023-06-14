import pygame
from pygame.locals import *

from Vector2 import *
from Vector3 import *

def drawTriangle(surface,_ver1,_ver2,_ver3):
    #Sorting all vertex from high to low , left to right
    if compare(_ver2,_ver1) == True : _ver1 , _ver2 = swap(_ver1,_ver2)
    if compare(_ver3,_ver1) == True : _ver1 , _ver3 = swap(_ver1,_ver3)
    if compare(_ver3,_ver2) == True : _ver2 , _ver3 = swap(_ver2,_ver3)

    ##Debugging Print Vertex After Sorting
    #font = pygame.font.Font(None, 36)
    #text_surface = font.render('V1', True, (0, 0, 0))  # Black
    #surface.blit(text_surface, (_ver1.x, _ver1.y))

    #text_surface = font.render('V2', True, (0, 0, 0))  # Black
    #surface.blit(text_surface, (_ver2.x, _ver2.y))

    #text_surface = font.render('V3', True, (0, 0, 0))  # Black
    #surface.blit(text_surface, (_ver3.x, _ver3.y))

    #Early return if there's no traiangle
    if _ver1.y == _ver2.y :
        return
    #False/0 = Left , True/1 = Right
    bShortSide = ((_ver2.y - _ver1.y) * (_ver3.x - _ver1.x)) < ((_ver2.x - _ver1.x) * (_ver3.y - _ver1.y))
    side = [0 for _ in range(2)]
    side[not bShortSide] = makeSlope(_ver1,_ver3,_ver3.y-_ver1.y)

    #Drawing Triangle
    y = _ver1.y
    yEnd = _ver1.y
    while y < _ver3.y :
        if (y >= yEnd) :
            side[bShortSide] = makeSlope(_ver1,_ver2,(yEnd:=_ver2.y)-_ver1.y) if (y < _ver2.y) else makeSlope(_ver2,_ver3,(yEnd:=_ver3.y)-_ver2.y)
        side[0],side[1] = DrawLine(surface,y,side[0],side[1])
        y+=1
    return

def makeSlope(V1,V2,numStep) :
    return [V1.x , (V2.x-V1.x)/numStep]

def DrawLine(surface ,y , left , right) :
    xStart,xStop = int(left[0]) , int(right[0])
    while xStart < xStop :
        setPixel(surface,xStart,y,(0,0,0))
        xStart+=1
    return [left[0]+left[1] , left[1]],[right[0]+right[1] , right[1]]

def compare(a,b):
    if a.y < b.y or ( (a.y == b.y) and (a.x < b.x) ) :
        return True
    return False

def swap(a, b):
    return b, a

def setPixel(surface,x,y,color):
    surface.set_at((x, int(y)), color)
    return
