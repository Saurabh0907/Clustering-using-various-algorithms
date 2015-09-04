from numpy import *
import sys, math, random
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv

class Point:
    def __init__(self, coords, reference=None):
        self.coords = coords
        self.n = len(coords)
        self.reference = reference
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
    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        return getDistance(old_centroid, self.centroid)
    def calculateCentroid(self):
        reduce_coord = lambda i:reduce(lambda x,p : x + p.coords[i],self.points,0.0)    
        centroid_coords = [reduce_coord(i)/len(self.points) for i in range(self.n)] 
        return Point(centroid_coords)

def kmeans(points, k, cutoff):
    initial = random.sample(points, k)
    clusters = [Cluster([p]) for p in initial]
    while True:
        lists = [ [] for c in clusters]
        for p in points:
            smallest_distance = getDistance(p,clusters[0].centroid)
            index = 0
            for i in range(len(clusters[1:])):
                distance = getDistance(p, clusters[i+1].centroid)
                if distance < smallest_distance:
                    smallest_distance = distance
                    index = i+1
            lists[index].append(p)
        biggest_shift = 0.0
        for i in range(len(clusters)):
            shift = clusters[i].update(lists[i])
            biggest_shift = max(biggest_shift, shift)
        if biggest_shift < cutoff: 
            break
    return clusters

def getDistance(a, b):
    if a.n != b.n: raise Exception("ILLEGAL: non comparable points")
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.sqrt(ret)

x=-1;

def makePoint(x_list, y_list):
    global x;
    x=x+1;
    return Point([float(x_list[x]), float(y_list[x])]);

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
    points = map( lambda i: makePoint(x_list, y_list), range(num_points) )
    
    clusters = kmeans(points, k, cutoff)
    
    colors_arr = []
    for c in colors.cnames:
        colors_arr.append(c);
    
    for i,c in enumerate(clusters):
        for p in c.points:
            #print " Cluster: ",i,"\t Point :", p
            plt.scatter(p.coords[0], p.coords[1], color= colors_arr[i]);
    plt.show()

if __name__ == "__main__": 
    main()