# /usr/bin/python
from scipy.stats import mode
from scipy.spatial import ConvexHull
import numpy as np
import math
import cv2
from constants import TRAINING_LOCATION, CACHED_LOCATION, SHAPE


def polyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def perimeter(points):
    p = 0
    for i in range(len(points) - 1):
        a = points[i][0] - points[i + 1][0]
        b = points[i][1] - points[i + 1][1]
        p = p + math.sqrt(a ** 2 + b ** 2)
    return p


def minimum_bounding_rectangle(points):
    """
    Find the smallest bounding rectangle for a set of points.
    Returns a set of points representing the corners of the bounding box.

    :param points: an nx2 matrix of coordinates
    :rval: an nx2 matrix of coordinates
    """
    from scipy.ndimage.interpolation import rotate
    pi2 = np.pi / 2.

    # get the convex hull for the points
    hull_points = points[ConvexHull(points).vertices]

    # calculate edge angles
    edges = np.zeros((len(hull_points) - 1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    # find rotation matrices
    # XXX both work
    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles - pi2),
        np.cos(angles + pi2),
        np.cos(angles)]).T
    #     rotations = np.vstack([
    #         np.cos(angles),
    #         -np.sin(angles),
    #         np.sin(angles),
    #         np.cos(angles)]).T
    rotations = rotations.reshape((-1, 2, 2))

    # apply rotations to the hull
    rot_points = np.dot(rotations, hull_points.T)

    # find the bounding points
    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    # find the box with the best area
    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    # return the best box
    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)

    area = abs(y2 - y1) * abs(x2 - x1)
    per = 2 * (abs(y2 - y1) + abs(x2 - x1))
    return per, area


def minimum_bounding_circle(points):
    """
    Find the smallest bounding rectangle for a set of points.
    Returns a set of points representing the corners of the bounding box.

    :param points: an nx2 matrix of coordinates
    :rval: an nx2 matrix of coordinates
    """
    c, radius = cv2.minEnclosingCircle(points)
    return np.pi * (radius ** 2), 2 * np.pi * radius


def areaTriange(p1, p2, p3):
    """
    Determines the area of triangle formed by 3 points (x,y)
    """
    d1 = p1[0] - p2[0]
    d2 = p1[1] - p2[1]
    a = math.sqrt(d1 ** 2 + d2 ** 2)
    d1 = p2[0] - p3[0]
    d2 = p2[1] - p3[1]
    b = math.sqrt(d1 ** 2 + d2 ** 2)
    d1 = p1[0] - p3[0]
    d2 = p1[1] - p3[1]
    c = math.sqrt(d1 ** 2 + d2 ** 2)
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    return area


def maxTriange(points):
    """
    Returns the area of the largest triangle that can be formed inside given ConvexHull
    """
    n = len(points) - 1
    A = 0;
    B = 1;
    C = 2
    bA = A;
    bB = B;
    bC = C  # The "best" triple of points
    while True:  # loop A

        while True:  # loop B
            while areaTriange(points[A], points[B], points[C]) <= areaTriange(points[A], points[B],
                                                                              points[(C + 1) % n]):  # loop C
                C = (C + 1) % n
            if areaTriange(points[A], points[B], points[C]) <= areaTriange(points[A], points[(B + 1) % n], points[C]):
                B = (B + 1) % n
                continue
            else:
                break

        if areaTriange(points[A], points[B], points[C]) > areaTriange(points[bA], points[bB], points[bC]):
            bA = A;
            bB = B;
            bC = C

        A = (A + 1) % n
        if A == B:
            B = (B + 1) % n
        if B == C:
            C = (C + 1) % n
        if A == 0:
            break
    return areaTriange(points[bA], points[bB], points[bC])


def extract_features(points):
    """
    Extracts the features from given array of x,y coordinates
    @param points: Array of x,y coordinates.
    @returns: array of features.
    """
    feature = []
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]
    area = polyArea(x, y)
    per = perimeter(points)
    if area > 0:
        feature.append(per ** 2 / area)
        triangle_area = 1
        triangle_area, p = minimum_bounding_circle(points)
        feature.append(triangle_area / area)
        rect_p, rect_a = minimum_bounding_rectangle(points)
        feature.append(per / rect_p)
        feature.append(area ** 2 / (rect_a * triangle_area))
        return feature


def extract_features_xy(x, y):
    """
    Extracts the features from given array of x,y coordinates
    @param points: Array of x,y coordinates.
    @returns: array of features.
    """
    feature = []
    points = np.column_stack((x, y))
    x = points[:, 0]
    y = points[:, 1]
    area = polyArea(x, y)
    per = perimeter(points)
    if area > 0:
        feature.append(per ** 2 / area)
        triangle_area, p = minimum_bounding_circle(points)
        feature.append(triangle_area / area)
        rect_p, rect_a = minimum_bounding_rectangle(points)
        feature.append(per / rect_p)
        feature.append(area ** 2 / (rect_a * triangle_area))
        return feature


def innerproduct(X, Z=None):
    if Z is None:  # case when there is only one input (X)
        Z = X
    return np.inner(X, Z)


def l2distance(X, Z=None):
    """
    function D=l2distance(X,Z)
    
    Computes the Euclidean distance matrix.
    Syntax:
    D=l2distance(X,Z)
    Input:
    X: nxd data matrix with n vectors (rows) of dimensionality d
    Z: mxd data matrix with m vectors (rows) of dimensionality d
    
    Output:
    Matrix D of size nxm
    D(i,j) is the Euclidean distance of X(i,:) and Z(j,:)
    
    call with only one input:
    l2distance(X)=l2distance(X,X)
    """
    if Z is None:
        Z = X
    G = innerproduct(X, Z)
    x, z = G.shape
    x1 = np.dot(np.diagonal(innerproduct(X)).reshape(x, 1), np.ones((1, z)))
    z1 = np.dot(np.diag(innerproduct(Z)).reshape(z, 1), np.ones((1, x)))
    D = np.sqrt(abs(x1 + z1.T - 2 * innerproduct(X, Z)))
    return D


def findknn(xTr, xTe, k):
    """
    function [indices,dists]=findknn(xTr,xTe,k);
    
    Finds the k nearest neighbors of xTe in xTr.
    
    Input:
    xTr = nxd input matrix with n row-vectors of dimensionality d
    xTe = mxd input matrix with m row-vectors of dimensionality d
    k = number of nearest neighbors to be found
    
    Output:
    indices = kxm matrix, where indices(i,j) is the i^th nearest neighbor of xTe(j,:)
    dists = Euclidean distances to the respective nearest neighbors
    """
    dist = l2distance(xTe, xTr)
    asd = np.argsort(dist)
    indices = asd[:, :k].T
    sd = np.sort(dist)
    dists = sd[:, :k].T

    return indices, dists


def analyze(kind, truth, preds):
    """
    function output=analyze(kind,truth,preds)         
    Analyses the accuracy of a prediction
    Input:
    kind='acc' classification error
    kind='abs' absolute loss
    (other values of 'kind' will follow later)
    """
    truth = truth.flatten()
    preds = preds.flatten()

    if kind == 'abs':
        loss = np.absolute(np.subtract(truth, preds))
        output = np.divide(np.float(np.sum(loss)), np.size(truth))
    elif kind == 'acc':
        correct = np.equal(truth, preds)
        output = np.divide(np.float(np.sum(correct)), np.size(truth))

    return output


def knnclassifier(xTr, yTr, xTe, k):
    """
    function preds=knnclassifier(xTr,yTr,xTe,k);
    
    k-nn classifier 
    
    Input:
    xTr = nxd input matrix with n row-vectors of dimensionality d
    xTe = mxd input matrix with m row-vectors of dimensionality d
    k = number of nearest neighbors to be found
    
    Output:
    
    preds = predicted labels, ie preds(i) is the predicted label of xTe(i,:)
    """
    if k % 2 == 0 and k > 1:
        k = k - 1
    indices, distances = findknn(xTr, xTe, k)
    yTr = np.array(yTr)
    a = yTr[indices]
    preds = mode(a, axis=0)
    return preds[0].flatten()


def getTrainingData():
    """
    Utility function to get training data and parse into desired format.
    Returns:
    Raw data converted to feature vector and its corresponding labelling yTr
    """
    data = []
    feature_vector = []
    yTr = []

    cachedFeatures = open(CACHED_LOCATION)
    line = cachedFeatures.readline()
    cachedFeatures.close()
    #Note: if everything's okay should say cache ready
    # the strips() make sure that spaces don't result in a false inequality
    if line.strip() == "cache ready!\n".strip():
        #print ("Getting cached features")
        feature_vector, yTr = getCachedFeatures()
    else:
        print ("No cache present")
    #print ("feature = " + str(feature_vector))
    #print ("ytr = " + str(yTr))

    if yTr != -1:
        # loading successful
        return feature_vector, yTr
    else:
        feature_vector, yTr = []

    f = open(TRAINING_LOCATION)
    a = f.readlines()

    for l in a:
        p = 0
        tmp = l.strip()
        tmp = eval(tmp)
        s = SHAPE[tmp[-1]]

        points = np.array(tmp[:-1])
        feat = extract_features(points)
        if feat:
            feature_vector.append(feat)
            yTr.append(s)

    return feature_vector, yTr


def getCachedFeatures():
    data = []
    feature_vector = []
    featuresParsed = []
    yTr = []

    cachedFeatures = open(CACHED_LOCATION)
    a = cachedFeatures.readlines()

    if a[0].strip() != "cache ready!\n".strip():
        print("failed to load cache")
        return feature_vector, -1

    for l in a[1:]:
        p = 0
        tmp = l.strip()
        featuresString, yTrString = tmp.split(";")
        featuresString = featuresString.split(",")

        for feature in featuresString:
            featuresParsed.append(float(feature))

        feature_vector.append(featuresParsed)
        featuresParsed = []

        yTr.append(int(yTrString))

        #print (str(l))

    #print("Returning cache")
    return feature_vector, yTr


def cacheFeatures():
    """
    Utility function to get training data and parse into desired format writing it to file.
    Writes to file:
    Raw data converted to feature vector and its corresponding labelling yTr
    """
    f = open(TRAINING_LOCATION)
    a = f.readlines()
    data = []
    feature_vector = []
    yTr = []
    cachedFeatures = open(CACHED_LOCATION, "r+")
    cachedFeatures.write("cache ready!\n")

    for l in a:
        p = 0
        tmp = l.strip()
        tmp = eval(tmp)
        s = SHAPE[tmp[-1]]

        # if tmp[-1] in ("loops"):
        # print("Lib: " + tmp[-1])
        # print("tiraste os loops")
        #    continue       

        points = np.array(tmp[:-1])
        features = extract_features(points)
        splitter = ","

        if features:
            for i in range(0, len(features)):
                if i == len(features) - 1:
                    splitter = ""
                cachedFeatures.write("{:.9f}".format(features[i]) + splitter)

            cachedFeatures.write(";" + str(s) + "\n")


def predict(inp):
    """
    Method to classify (predict) the shape based on given input.
    """
    xTe = [inp]
    feature_vector, yTr = getTrainingData()
    preds = knnclassifier(feature_vector, yTr, xTe, 1)

    return preds
