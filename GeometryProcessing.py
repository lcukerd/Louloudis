import math
import numpy as np
from sympy import Line, Point
from statistics import mean

try:
    import globalVar
except ModuleNotFoundError:
    import Louloudis.globalVar as globalVar

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
        if (dist < 2):
            ntemp +=1
    return ntemp

def findbelongCC(line, centroidsP, centroids, mapP):
    x1, x2, y1, y2 = findLine(line[0]-5, line[1]);
    x3, x4, y3, y4 = findLine(line[0]+5, line[1]);
    value = np.zeros((len(centroids)));
    for i in range(len(centroidsP)):
        centroid = centroidsP[i];
        if (encloses([x1, y1], [x2, y2], [x3, y3], [x4, y4], [centroid[0], centroid[1]])):
            value[mapP[i]] += 1;
        else:
            value[mapP[i]] -= 1;
    cc = [];
    for i in range(len(centroids)):
        if value[i] >= 0:
            cc.append(i);
    return cc

def discardPartition(line, centroidsP, centroids, mapP):
    cc = findbelongCC(line, centroidsP, centroids, mapP);
    count = 0;
    for i in range(len(centroidsP)):
        if mapP[i] in cc and centroidsP[i][0] != -1 and centroidsP[i][1] != -1:
            centroidsP[i] = (-1,-1);
            count += 1;
    return centroidsP, count

def findLine(rho, theta):
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho

    x1 = int(x0 + 10000*(-b))
    y1 = int(y0 + 10000*(a))
    x2 = int(x0 - 10000*(-b))
    y2 = int(y0 - 10000*(a))

    return x1, x2, y1, y2

def encloses(p1, p2, p3, p4, p5):
    p1 = np.array(p1);
    p2 = np.array(p2);
    p3 = np.array(p3);
    p4 = np.array(p4);
    p5 = np.array(p5);

    from1 = np.cross(p2-p1, p1-p5)/np.linalg.norm(p2-p1);
    from2 = np.cross(p4-p3, p3-p5)/np.linalg.norm(p4-p3);

    if from1 * from2 != abs(from1 * from2):
        return True;
    else:
        return False;

def findDistance(x1, x2, x3, y1, y2, y3):
    p1 = np.array([x1,y1])
    p2 = np.array([x2,y2])
    p3 = np.array([x3,y3])
    return np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)

def getLine(line):
    rho = line[0]
    theta = line[1]
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 10000*(-b)), int(y0 + 10000*(a)))
    pt2 = (int(x0 - 10000*(-b)), int(y0 - 10000*(a)))
    return Line(pt1, pt2);

def isAdjacent(linei, linej):
    startLine = Line((0,0),(0,100));
    (_, yi) = linei.intersection(startLine)[0];
    (_, yj) = linej.intersection(startLine)[0];

    if abs(yi-yj) < 100:
        return True;
    else:
        return False;

def getIntersections(lines, image):
    (h, w) = np.shape(image);
    Slines = []
    for line in lines:
        Slines.append(getLine(line));

    lineProcessed = [];
    distances = [];
    count = 0;
    for i in range(len(Slines)):
        if i in lineProcessed:
            continue;
        lineProcessed.append(i);
        count += 1;
        for j in range(len(Slines)):
            if j in lineProcessed:
                continue;

            linei = Slines[i];
            linej = Slines[j];
            if isAdjacent(linei, linej):
                inter = linei.intersection(linej);
                if inter != []:
                    inter = inter[0];
                else:
                    continue
                if inter.x < w and inter.x > 0:
                    lineProcessed.append(j);
                    distances.append( int(inter.distance(Point(w/2, inter.y))));

    return count;
