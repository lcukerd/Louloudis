import numpy as np

def init(lines, centroids):
    global dists
    dists = np.zeros((len(lines), len(centroids))) - 1;
    dists.shape;

def check(msg):
    global checkmsg
    checkmsg = msg;
