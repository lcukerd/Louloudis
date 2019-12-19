import math
import numpy as np
import globalVar

from sympy import Point, Polygon
from sympy.geometry import Segment, Line

def findValueofcell(line, centroids, lpos):
    ntemp = 0

    x1, x2, y1, y2 = findLine(line[0], line[1])

    for i in range(len(centroids)):
        pt = centroids[i]
        x3 = int(pt[0])
        y3 = int(pt[1])
        if (x3 == -1 and y3 == -1):
            continue;
        if (globalVar.dists[lpos][i] == -1):
            dist = findDistance(x1, x2, x3, y1, y2, y3);
            globalVar.dists[lpos][i] = dist;
        else:
            dist = globalVar.dists[lpos][i];
        if (dist < 5):
            ntemp +=1
    return ntemp

def findLine(rho, theta):
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho

    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    return x1, x2, y1, y2

def findDistance(x1, x2, x3, y1, y2, y3):
    line = Line((x1,y1), (x2,y2))
    point = Point (x3, y3)
    return line.distance(point)
