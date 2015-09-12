import subprocess
from numpy import *
import sys, math, random
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv
import scipy.stats as st;

x=-1;

def getNormDistance(a, b):
    if a.n != b.n:
        raise Exception("ILLEGAL: non comparable points")
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.fabs(ret)

def getDistance(a, b):
    if a.n != b.n:
        raise Exception("ILLEGAL: non comparable points")
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.sqrt(ret)

def makePoint(x_list, y_list):
    global x;
    x=x+1;
    return Point([float(x_list[x]), float(y_list[x])]);

class Point:
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)        
    def __repr__(self):
        return str(self.coords)

class Cluster:
    def __init__(self, points):
        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        self.points = points
        self.n = points[0].n
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")
        self.centroid = self.calculateCentroid()
    def __repr__(self):
        return str(self.points)
    def size(self):
        count = 0;
        for p in self.points:
            count = count + 1;
        return count;
    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid) 
        return shift
    def calculateCentroid(self):
        numPoints = len(self.points)
        coords = [p.coords for p in self.points]
        unzipped = zip(*coords)
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]
        return Point(centroid_coords)

def kmeans(points, k, cutoff, colors_arr):
    initial = random.sample(points, k)
    clusters = [Cluster([p]) for p in initial]
    
    loopCounter = 0
    while True:
        lists = [ [] for c in clusters]
        clusterCount = len(clusters)
        
        loopCounter += 1
        for p in points:
            smallest_distance = getDistance(p, clusters[0].centroid)
            clusterIndex = 0
            for i in range(clusterCount - 1):
                distance = getDistance(p, clusters[i+1].centroid)
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            lists[clusterIndex].append(p)
        
        biggest_shift = 0.0
        
        for i in range(clusterCount):
            shift = clusters[i].update(lists[i])
            biggest_shift = max(biggest_shift, shift)
        
        #for i,c in enumerate(clusters):
        #    for p in c.points:
        #        plt.scatter(p.coords[0], p.coords[1], color= colors_arr[i]);
        
        #plt.savefig('figure' + str(loopCounter) + '.png');
        
        if biggest_shift < cutoff:
            print "Converged after %s iterations" % loopCounter
            break
    return clusters


def main():
    f = open('real_1.csv', 'rU');

    x_list = [];
    y_list = [];
    
    for line in f:
        cells = line.split(",");
        x_list.append(cells[0]);
        y_list.append(cells[1]);
    
    x_list = x_list[1:];
    y_list = y_list[1:];

    num_points, k, cutoff = len(x_list), 5, 0.5
    points = [makePoint(x_list, y_list) for i in xrange(num_points)]

    colors_arr = []
    for c in colors.cnames:
        colors_arr.append(c);
    
    clusters = kmeans(points, k, cutoff, colors_arr)

    confidence_level=0.95;
    z_score = math.fabs(st.norm.ppf((1-confidence_level)/2));

    for i,c in enumerate(clusters):
        
        count = 0;
        print "Centroid :"+str(c.centroid);
        print str(c.size());
        
        stan_dev = math.sqrt(sum(getNormDistance(c.centroid,p) for p in c.points)/c.size());
        
        margin_of_error = z_score * (stan_dev/math.sqrt(c.size()));
        
        print "Error :"+str(margin_of_error);
        
        for p in c.points:
            if (p.coords[1] <= margin_of_error):
                plt.scatter(p.coords[0], p.coords[1], color= colors_arr[i]);
            else:
                plt.scatter(p.coords[0], p.coords[1], color= 'BLACK');
    plt.show()

if __name__ == "__main__": 
    main()