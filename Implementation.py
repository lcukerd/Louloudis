import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import math

from Processing import *
from ImageHandler import *
from GeometryProcessing import *
from ImageProcessing import *
from globalVar import *

def performLouloudisSegmentation(file_name):
    image = loadImage(file_name);

    (labels, avg_height, centroids, stats) = findComponents(image);
    ((centroids1, stats1), (centroids2, stats2), (centroids3, stats3)) = divide(centroids, stats, avg_height);

    centroidP, mapP = partitionCCH(stats1, int (avg_height));

    lines = findHoughLines(showCentroids(image, centroidP), None, avg_height, 100, 10, 40)
    init(lines, centroidP);

    n = 1000;
    selLines = [];
    while (True):
        lineP, pos, n = findPrimaryCell(lines, centroidP);
        print ("\n Contribution " + str(n), end= " ");
        if n < 5:
            break;
        elif n < 9:
            pTheta = math.radians(selLines[0][1]);
            theta = math.radians(lineP[1]);
            if (not (theta <= pTheta + 2 and theta >= pTheta - 2)):
                continue;
            print ("Low Contribution " + str(n), end = " ");

        centroidPN, count = discardPartition(lineP, np.copy(centroidP), centroids1, mapP)

        print ("Discarded " + str(count) + " centroids");

        centroidP = np.copy(centroidPN);
        selLines.append(lineP);

    print (str(len(selLines)) + " lines selected");

    return len(selLines);