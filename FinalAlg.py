# import necessary dependencies
from enum import Enum
import csv
import random
import numpy
import math

grid = []
# create a lovely enum to hold directions in
class Direction(Enum):
    TOP = 90
    TOP_RIGHT = 45
    RIGHT = 0
    BOTTOM_RIGHT = 315
    BOTTOM = 270
    BOTTOM_LEFT = 225
    LEFT = 180
    TOP_LEFT = 135

    def __int__(self):
        return self.value


# create Node class
class Node:
    def __init__(self, x, y, height, prevDir):
        self.x = x
        self.y = y
        self.height = height
        self.prevDir = prevDir

    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

# create custom Individual class
class Path:
    # takes as args a list of Nodes
    def __init__(self, route):
        self.route = route
    def addToPath(self, n):
        self.route.append(n)
    def __iter__(self):
        return self
    def __next__(self):
        num = self.num
        self.num += 1
        return num
    def printPath(self):
        ret = ""
        for i in self.route:
            ret +=(i.toString()) + " | "
        return ret

#Cleans up random walk. Eliminates loops. Variable effectiveness depending on the random walk
def cleanup(p1):
    i = 0
    j = 0
    flag = False
    while i < len(p1) :
        for j in range(len(p1)):
            for h in reversed(range(len(p1), 0, -1)):
                if j < h and j < len(p1) and h < len(p1) and p1[h] == p1[j] and j != h:
                    p1 = p1[:j] + p1[h:]
                    print("h : " + str(h) + ", i : " + str(i) + ", j : " + str(j))
                    i = 0
                    flag = True
                    if(flag):
                        break
        i += 1
    return p1

# returns index of the crossover point in p1 and in p2 as tuple
# takes two Paths as params
def pathsCross(p1, p2):
    for i in range(0, len(p1.route)):
        for j in range(0, len(p2.route)):
            if i.equals(j):
                cross = (i, j)
            else:
                cross = (-1, -1)
    return cross

# returns a tuple containing two Path objects
# takes two Path objects as params
def breed(p1, p2):
    child1 = list()
    child2 = list()
    parent1 = p1.route
    parent2 = p2.route
    crosspt = pathsCross(p1, p2)
    if crosspt != (-1, -1):
        child1.append(parent1[:crosspt[0]])
        child1.append(parent2[crosspt[1]:])
        child2.append(parent2[:crosspt[1]])
        child2.append(parent1[crosspt[0]:])
    kids = (Path(child1), Path(child2))
    return kids


def mutate(p1, mutateFactor=0.2):
    for x in range(1, len(p1) - 1):
        if random.randint(1, 10) < (mutateFactor * 10) and x - 1 > 0 and x + 1 < 49:
            oldX = p1[x].x
            oldY = p1[x].y
            global grid
            xoffset = 0
            yoffset = 0
            if ((p1[x].prevDir == Direction.TOP and p1[x + 1].prevDir == Direction.TOP) or \
                     (p1[x].prevDir == Direction.BOTTOM and p1[x + 1].prevDir == Direction.BOTTOM)):
                flag = random.randint(0, 1)
                if (flag == 1):
                    xoffset = 1
                else:
                    xoffset = -1
            if ((p1[x].prevDir == Direction.RIGHT and p1[x + 1].prevDir == Direction.RIGHT) or \
                    (p1[x].prevDir == Direction.LEFT and p1[x + 1].prevDir == Direction.LEFT)):
                flag = random.randint(0, 1)
                if (flag == 1):
                    yoffset = 1
                else:
                    yoffset = -1

            cost = calcWeights(p1[x - 1], p1[x]) + calcWeights(p1[x], p1[x + 1])
            newCost = cost

            if p1[x].x + xoffset > 0 and p1[x].x + xoffset < 49 and \
                    p1[x].y + yoffset > 0 and p1[x].y + yoffset < 49:

                newNode = grid[p1[x].y + yoffset][p1[x].x + xoffset]

                newCost = calcWeights(p1[x - 1], newNode) + calcWeights(newNode, p1[x+1])
                print("Mutating x by : " + str(xoffset) + "   Mutating y by : " + str(yoffset) + " at " + "(" + str(oldX) +"," + str(oldY) + ")")
            if newCost < cost:
                p1[x] = newNode


# Calculates the weights between nodes based on curvature,
# distance, travel time, and cost to create
# dataPointOffset is the real-world distance between two data points on the same orthogonal line IN FEET
# distWeight, timeWeight, and costWeight must sum to 1.0
def calcWeights(node1, node2, dataPointOffset = 100, distWeight = 0.3, inclWeight = 0.2, costWeight = 0.2):
    # Average cost of a mile of 4-land divided highway through semi-urban
    # and non-mountainous terrain
    # See https://www.arkansashighways.com/roadway_design_division/Cost%20per%20Mile%20(JULY%202014).pdf
    # for details
    COST_PER_MILE = 5675000

    # avgSpeed is the average speed limit of US 4-lane divided highways by default, but
    # can be changed if desired
    # CHANGE THIS FROM 3D DISTANCE TO 2D DIST AND CALCULATE ELEVATION DIFF
    # TO DEAL W/ROAD GRADING
    grade = abs(int(node1.height) - int(node2.height))
    xdiff = abs(node1.x - node2.x) * dataPointOffset
    ydiff = abs(node1.y - node2.y) * dataPointOffset
    dist = (xdiff)**2 + (ydiff)**2
    if(dist < 1):
        dist = 1
    dist = math.sqrt(dist)
    grade = (grade / dist) * 100 # grade as percentage

    sum = dist * distWeight + grade * inclWeight

    # difference in road angles: higher = less direct route
    curve = abs(node1.prevDir.value - node2.prevDir.value) % 360
    cfactor = (360 - curve) if curve > 180 else curve

    # calculate highway segment speed based on curvature
    # V**2  = 15(0.01 * e + f) * R
    # side-friction constants from:
    # https://www.webpages.uidaho.edu/niatt_labmanual/chapters/geometricdesign/theoryandconcepts/SuperElevationAndSideFriction.htm
    # Formula from:
    # https://safety.fhwa.dot.gov/speedmgt/ref_mats/fhwasa1122/ch3.cfm

    # superelevation information
    # https://safety.fhwa.dot.gov/geometric/pubs/mitigationstrategies/chapter3/3_superelevation.cfm
    # f = 0.10 # side friction constant
    # R = 2740
    # vsquared = 15 * (f + 0.06) * R
    # v = math.sqrt(vsquared)
    CURVE_SPEED = 53.64 # determined by above calculations
    if cfactor > 0: # if road curves
        # reduce speed to curve speed
        travelTime = dist / CURVE_SPEED
        COST_PER_MILE *= 1.1
    else:
        travelTime = dist / 65
    # add in cost of the road and curvature factors
    sum += dist * COST_PER_MILE * costWeight + travelTime
    return sum

def main():
    # Node Generation
    width = 50
    height = 50
    blank = Node(0, 0, 0, 0)
    global grid
    grid = [[blank for x in range(width)] for y in range(height)]
    with open("C:\\Users\\nelsonmp\\testInput.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        d = list(reader)

    i = 0  # height / y
    # print(d[9][11])
    for k in d:
        l = 0  # width / x
        for j in k:
            grid[i][l] = Node(l, i, d[i][l], Direction.RIGHT)
            l += 1
        i += 1

    print(grid[0][0].x)
    print(grid[0][0].y)
    print(grid[49][49].prevDir)
    print(grid[49][49].height)  # last node
    # read in data from file,
    # store data in 'graph'
    # Create starting population of paths via random walk
    # Mutate paths
    # Breeding (and culling) stage
    # Profit
    crossProb = 0.2
    mutProb = 0.2
    generations = 0
    pop = list()
    startPop = 20 # starting population size

    startNode = grid[0][0] # fist city here
    endNode = grid[4][4] # second city here
    
    # these are vars for dimensions of our array:
    # put actual data here after reading data in from file
    nodeToAdd = None
    # now for the randomwalk
    #
    #    7     0     1
    #     \    |    /
    #    6-   Node  -2
    #     /    |    \
    #    5     4     3
    #

    startingPath = list()
    for i in range(startPop):
        lastNode = startNode
        prevDir = 2
        startNode = grid[0][0]  # fist city here
        endNode = grid[4][4]  # second city here
        nodeToAdd = None
        #random.seed( 30 )
        while nodeToAdd != endNode:
            dir = random.randint(0, 7)
            xoffset = 0
            yoffset = 0
            if dir == 0 :
                xoffset = 0
                yoffset = -1
                prevDir = dir
            elif dir == 1 :
                xoffset = 1
                yoffset = -1
                prevDir = dir
            elif dir == 2 :
                xoffset = 1
                yoffset = 0
                prevDir = dir
            elif dir == 3 :
                xoffset = 1
                yoffset = 1
                prevDir = dir
            elif dir == 4 :
                xoffset = 0
                yoffset = 1
                prevDir = dir
            elif dir == 5 :
                xoffset = -1
                yoffset = 1
                prevDir = dir
            elif dir == 6 :
                xoffset = -1
                yoffset = 0
                prevDir = dir
            elif dir == 7 :
                xoffset = -1
                yoffset = -1
                prevDir = dir
            else:
                xoffset = 1
                yoffset = 1
            prevDir = dir
            if lastNode.x + xoffset < 5 and lastNode.x + xoffset > 0:
                if lastNode.y + yoffset < 5 and lastNode.y + yoffset > 0:
                    nodeToAdd = grid[lastNode.y + yoffset][lastNode.x + xoffset]
                    lastNode = nodeToAdd
                    startingPath.append(nodeToAdd)
        pop.append(Path(startingPath))
        startingPath = []

    print(len(pop[0].route))
    #print("x : " + str(pop[0].route[len(pop[0].route) - 1].x) + " y : " + str(pop[0].route[len(pop[0].route) - 1].y))

    print(pop[0].printPath())
    pop[0] = Path(cleanup(pop[0].route))

    print(pop[0].printPath())
    for x in range(20):
        mutate(pop[0].route)

    pop[0] = Path(cleanup(pop[0].route))
    print(pop[0].printPath())


if __name__ == "__main__":
    main()