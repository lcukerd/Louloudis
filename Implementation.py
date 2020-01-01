import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import math

try:
    from Processing import *
    from ImageHandler import *
    from GeometryProcessing import *
    from ImageProcessing import *
    from globalVar import *
except ModuleNotFoundError:
    from Louloudis.Processing import *
    from Louloudis.ImageHandler import *
    from Louloudis.GeometryProcessing import *
    from Louloudis.ImageProcessing import *
    from Louloudis.globalVar import *

def performLouloudisSegmentation(file_name, d):
    image = loadImage(file_name);

    (labels, avg_height, centroids, stats) = findComponents(image);
    ((centroids1, stats1), (centroids2, stats2), (centroids3, stats3)) = divide(centroids, stats, avg_height);

    centroidP, mapP = partitionCC(stats1, int (avg_height));

    lines = [];
    threshold = 10;
    while (len(lines) < 4 or len(lines) > 70) and threshold < 500:
        lines = findHoughLines(showCentroids(image, centroidP), None, avg_height, threshold, 10, 40)
        threshold += 5;
    if len(lines) < 4 or len(lines) > 100:
        return 0;

    init(lines, centroidP);

    n = 1000;
    selLines = [];
    while (True):
        lineP, pos, n = findPrimaryCell(lines, centroidP);
        lines[pos] = [(-1, -1)];
        if n < 5:
            break;
        elif n < 9 and selLines != []:
            pTheta = math.radians(selLines[0][1]);
            theta = math.radians(lineP[1]);
            if (not (theta <= pTheta + 2 and theta >= pTheta - 2)):
                continue;

        centroidPN, count = discardPartition(lineP, np.copy(centroidP), centroids1, mapP)

        centroidP = np.copy(centroidPN);
        if count != 0:
            selLines.append(lineP);

    return getIntersections(selLines, image);
