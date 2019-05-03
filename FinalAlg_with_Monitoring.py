# import necessary dependencies
from enum import Enum
import csv
import random
import matplotlib.pyplot as plt
import math
import time

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
    NOCHANGE = -1

    def __int__(self):
        return self.value


# create Node class
class Node:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

Node1 = Node(0, 0, 0)
Node2 = Node(0, 0, 0)
Node3 = Node(0, 0, 0)

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
            ret += i.toString() + " | "
        return ret


def pathPrinter(p1):
    ret = ""
    for i in p1.route:
        ret += grid[i.y][i.x].toString() + " | "
    return ret


# Cleans up random walk. Eliminates loops. Variable effectiveness depending on the random walk
def cleanup(p1):
    i = 0
    while i < len(p1):
        for j in range(len(p1)):
            for h in reversed(range(len(p1) - 1, 0, -1)):
                if j < h and j < len(p1) and h < len(p1) and p1[h] == p1[j] and j != h:
                    p1 = p1[:j] + p1[h:]
                    # print("h : " + str(h) + ", i : " + str(i) + ", j : " + str(j))
                    i = 0
                    break

        i += 1
    return p1


def prevDir(n1, n2):  # Finds the direction a path takes
    xChange = n2.x - n1.x
    yChange = n2.y - n1.y
    if xChange == 1:
        if yChange == 1:
            return Direction.BOTTOM_RIGHT
        elif yChange == 0:
            return Direction.RIGHT
        elif yChange == -1:
            return Direction.TOP_RIGHT
    elif xChange == 0:
        if yChange == 1:
            return Direction.BOTTOM
        elif yChange == -1:
            return Direction.TOP
    elif xChange == -1:
        if yChange == 1:
            return Direction.BOTTOM_LEFT
        elif yChange == 0:
            return Direction.LEFT
        elif yChange == -1:
            return Direction.TOP_LEFT
    elif xChange == 0 and yChange == 0:
        return Direction.NOCHANGE
    else:
        return Direction.NOCHANGE


# returns index of the crossover point in p1 and in p2 as tuple
# takes two Paths as params
def pathsCross(p1, p2):
    cross = (-1, -1)
    path1 = Path(p1.route)
    n = len(p2.route)
    for i in range(1, len(path1.route) - 1):
        for j in reversed(range(len(p2.route) - 1, 1, -1) ) :
            if p1.route[i] == p2.route[j]:
                cross = (i, j)
                return cross
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
        child1 = parent1[:crosspt[0]] + parent2[crosspt[1]:]
        child2 = parent2[:crosspt[1]] + parent1[crosspt[0]:]
    return Path(child1), Path(child2)


def mutate(p1, mutateFactor=0.1):
    # print("mutating")
    for x in range(len(p1) - 1 ):
        if random.randint(1, 10) <= (mutateFactor * 10) and x - 1 > 0 and x + 1 < 49:
            oldX = p1[x].x
            oldY = p1[x].y
            currentNode = p1[x]
            nextNode = p1[x + 1]
            pDir = prevDir(p1[x - 1], p1[x])
            cDir = prevDir(p1[x], p1[x + 1])
            global grid
            xoffset = 0
            yoffset = 0
            if ((pDir == Direction.TOP and cDir == Direction.TOP) or \
                    (pDir == Direction.BOTTOM and cDir == Direction.BOTTOM)):  # |
                flag = random.randint(0, 1)  # |
                if (flag == 1):
                    xoffset = 1
                else:
                    xoffset = -1
            elif ((pDir == Direction.RIGHT and cDir == Direction.RIGHT) or \
                  (pDir == Direction.LEFT and cDir == Direction.LEFT)):  # --
                flag = random.randint(0, 1)
                if (flag == 1):
                    yoffset = 1
                else:
                    yoffset = -1
            elif ((pDir == Direction.RIGHT and cDir == Direction.TOP) or \
                  (pDir == Direction.BOTTOM and cDir == Direction.LEFT)):  # _|
                yoffset = -1
                xoffset = -1
            elif ((pDir == Direction.BOTTOM_LEFT and cDir == Direction.TOP) or \
                  (pDir == Direction.BOTTOM and cDir == Direction.TOP_LEFT)):  # \|
                yoffsef = 0
                xoffset = -1
            elif ((pDir == Direction.TOP_RIGHT and cDir == Direction.BOTTOM_RIGHT) or \
                  (pDir == Direction.TOP_LEFT and cDir == Direction.BOTTOM_LEFT)):  # /\
                yoffset = 1
                xoffset = 0
            elif ((pDir == Direction.RIGHT and cDir == Direction.BOTTOM) or \
                  (pDir == Direction.TOP and cDir == Direction.LEFT)):  # -
                yoffset = 1  # |
                xoffset = -1
            elif ((pDir == Direction.BOTTOM_LEFT and cDir == Direction.RIGHT) or \
                  (pDir == Direction.LEFT and cDir == Direction.TOP_RIGHT)):  # /_
                yoffset = -1
                xoffset = 0

            elif ((pDir == Direction.BOTTOM_LEFT and cDir == Direction.BOTTOM_RIGHT) or \
                  (pDir == Direction.TOP_LEFT and cDir == Direction.TOP_RIGHT)):
                yoffset = 0
                xoffset = 1
            elif ((pDir == Direction.LEFT and cDir == Direction.BOTTOM_RIGHT) or \
                  (pDir == Direction.TOP_LEFT and cDir == Direction.RIGHT)):
                yoffset = 1
                xoffset = 0
            elif ((pDir == Direction.TOP and cDir == Direction.LEFT) or \
                  (pDir == Direction.LEFT and cDir == Direction.BOTTOM)):
                yoffset = 1
                xoffset = 1
            # Begin Wyatt's segment of ifs
            # CASE
            #  __       __
            #    \ and /
            elif ((pDir == Direction.RIGHT and cDir == Direction.BOTTOM_RIGHT) \
                  or (pDir == Direction.TOP_LEFT and cDir == Direction.LEFT)) \
                    or ((pDir == Direction.TOP and cDir == Direction.RIGHT) \
                        or (pDir == Direction.LEFT and cDir == Direction.BOTTOM_LEFT)):
                yoffset = 1
                xoffset = 0
            # CASE
            #  __/  and  \__
            elif ((pDir == Direction.RIGHT and cDir == Direction.TOP_RIGHT) \
                  or (pDir == Direction.LEFT and cDir == Direction.TOP_LEFT)) \
                    or ((pDir == Direction.BOTTOM_LEFT and cDir == Direction.LEFT) \
                        or (pDir == Direction.BOTTOM_RIGHT and cDir == Direction.RIGHT)):
                yoffset = -1
                xoffset = 0
            # CASE
            # |       /
            #  \ and |
            elif (pDir == Direction.BOTTOM and cDir == Direction.BOTTOM_RIGHT) \
                    or (pDir == Direction.TOP and cDir == Direction.TOP_RIGHT) \
                    or (pDir == Direction.TOP_LEFT and cDir == Direction.TOP) \
                    or (pDir == Direction.BOTTOM_LEFT and cDir == Direction.BOTTOM):
                yoffset = 0
                xoffset = 1
            # CASE
            # \       |
            #  | and /
            elif (pDir == Direction.BOTTOM_RIGHT and cDir == Direction.BOTTOM) \
                    or (pDir == Direction.TOP and cDir == Direction.TOP_LEFT) \
                    or (pDir == Direction.BOTTOM_LEFT and cDir == Direction.TOP) \
                    or (pDir == Direction.BOTTOM and cDir == Direction.BOTTOM_LEFT):
                yoffset = 0
                xoffset = -1
            # CASE
            # |\
            elif (pDir == Direction.TOP and cDir == Direction.BOTTOM_RIGHT) \
                    or (pDir == Direction.TOP_LEFT and cDir == Direction.BOTTOM):
                yoffset = 0
                xoffset = 1
            # CASE
            # /\ 90
            elif (pDir == Direction.TOP_RIGHT and cDir == Direction.BOTTOM_RIGHT) \
                    or (pDir == Direction.TOP_LEFT and cDir == Direction.BOTTOM_LEFT):
                yoffset = 1
                xoffset = 0
            # CASE
            # \/ 90
            elif (pDir == Direction.BOTTOM_RIGHT and cDir == Direction.TOP_RIGHT) \
                    or (pDir == Direction.BOTTOM_LEFT and cDir == Direction.TOP_LEFT):
                yoffset = -1
                xoffset = 0
            # CASE
            # __
            #  /
            elif (pDir == Direction.RIGHT and cDir == Direction.BOTTOM_LEFT) \
                    or (pDir == Direction.TOP_RIGHT and cDir == Direction.LEFT):
                yoffset = 1
                xoffset = 0
            # CASE
            # \ 90
            # /
            elif (pDir == Direction.BOTTOM_RIGHT and cDir == Direction.BOTTOM_LEFT) \
                    or (pDir == Direction.TOP_RIGHT and cDir == Direction.TOP_LEFT):
                yoffset = 0
                xoffset = -1
            cost = calcWeights(p1[x], p1[x - 1], p1[x - 2])
            newCost = cost
            if p1[x].x + xoffset > 1 and p1[x].x + xoffset < 49 and \
                    p1[x].y + yoffset > 1 and p1[x].y + yoffset < 49 and \
                    x - 1 > 0 and x + 1 < 49:

                newCost = calcWeights(p1[x - 1], grid[p1[x].y + yoffset][p1[x].x + xoffset], p1[x + 1])
                if newCost < cost:
                    p1[x] = grid[p1[x].y + yoffset][p1[x].x + xoffset]
                    # print("Mutating x by : " + str(xoffset) + "   Mutating y by : " + str(yoffset) + " at " + "(" + str(oldX) +"," + str(oldY) + ")")

#Calculate the cost of the full path
def calcCost(path):
    cost = 0
    cost += calcWeights(path.route[1], path.route[0], path.route[0])
    for i in range(2, len(path.route)): #cost += calcWeights(path.route[i], path.route[i], path.route[i])
        cost += calcWeights(path.route[i], path.route[i - 1], path.route[i-2])
    return cost

def sortPaths(paths):
    for i in range(len(paths)):
        for j in range(0, len(paths)-i-1):
            if calcCost(paths[j]) > calcCost(paths[j+1]):
                paths[j], paths[j + 1] = paths[j + 1], paths[j]
    return paths

def cull(paths, startPop = 20):
    paths = sortPaths(paths)
    return paths[:startPop]

# Calculates the weights between nodes based on curvature,
# distance, travel time, and cost to create
# dataPointOffset is the real-world distance between two data points on the same orthogonal line IN FEET
# distWeight, timeWeight, and costWeight must sum to 1.0
def calcWeights(node1, node2, node3, dataPointOffset=100, distWeight=0.3, inclWeight=0.2, costWeight=0.2):
    # node3 is previous node - only used for direction change
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
    dist = (xdiff) ** 2 + (ydiff) ** 2
    if (dist < 1):
        dist = 1
    dist = math.sqrt(dist)
    grade = (grade / dist) * 100  # grade as percentage

    sum = dist * distWeight + grade * inclWeight

    # difference in road angles: higher = less direct route
    if( node2.x != node3.x and node2.y != node3.y and node1.x != node2.x and node1.y != node2.y):
        curve = abs(prevDir(node1, node2).value - prevDir(node2, node3).value) % 360
    else:
        curve = 0
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
    CURVE_SPEED = 53.64  # determined by above calculations
    if cfactor > 0:  # if road curves
        # reduce speed to curve speed
        travelTime = dist / CURVE_SPEED
        COST_PER_MILE *= 1.1
    else:
        travelTime = dist / 65
    # add in cost of the road and curvature factors
    sum += dist * (COST_PER_MILE / 5280) * costWeight + travelTime
    return sum

#Mutate > Breed > Cleanup

def createNextGen(paths):
    for i in range(len(paths)):
        path = Path(paths[i].route)
        mutate(path.route)             #Mutates Path
    n = len(paths)
    for j in range(n - 1):                         #Breeds Paths
        for k in range(n - 1) :
            newPath1, newPath2 = breed(Path(paths[j].route), Path(paths[k].route))
            paths.append(Path(newPath1.route))
            paths.append(Path(newPath2.route))

    for h in range(len(paths)):                         #cleanup
        paths[h] = Path(cleanup(paths[h].route))

    paths = cull(paths, 20)
    return paths

def main():
    # Start run timer
    t0 = time.perf_counter()
    # Keep track of fitness metrics for each generation
    maxCostPerGen = list()
    avgCostPerGen = list()
    # Node Generation
    width = 50
    height = 50
    blank = Node(0, 0, 0)
    global grid
    grid = [[blank for x in range(width)] for y in range(height)]
    with open("testInput.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        d = list(reader)

    i = 0  # height / y
    # print(d[9][11])
    for k in d:
        l = 0  # width / x
        for j in k:
            grid[i][l] = Node(l, i, d[i][l])
            l += 1
        i += 1

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
    startPop = 20  # starting population size

    startNode = grid[0][0]  # fist city here
    Node1 = startNode
    endNode = grid[9][9]  # second city here
    Node2 = endNode

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
        startNode = grid[0][0]  # fist city here
        endNode = grid[9][9]  # second city here
        nodeToAdd = None
        #random.seed( 30 )
        while nodeToAdd != endNode:
            dir = random.randint(0, 7)
            xoffset = 0
            yoffset = 0
            if dir == 0:
                xoffset = 0
                yoffset = -1
            elif dir == 1:
                xoffset = 1
                yoffset = -1
            elif dir == 2:
                xoffset = 1
                yoffset = 0
            elif dir == 3:
                xoffset = 1
                yoffset = 1
            elif dir == 4:
                xoffset = 0
                yoffset = 1
            elif dir == 5:
                xoffset = -1
                yoffset = 1
            elif dir == 6:
                xoffset = -1
                yoffset = 0
            elif dir == 7:
                xoffset = -1
                yoffset = -1
            else:
                xoffset = 1
                yoffset = 1
            if lastNode.x + xoffset < 10 and lastNode.x + xoffset > 0:
                if lastNode.y + yoffset < 10 and lastNode.y + yoffset > 0:
                    nodeToAdd = grid[lastNode.y + yoffset][lastNode.x + xoffset]
                    lastNode = nodeToAdd
                    startingPath.append(nodeToAdd)
        pop.append(Path(startingPath))
        # print("Start route len: " + str(len(startingPath)))
        startingPath = []

    # print("x : " + str(pop[0].route[len(pop[0].route) - 1].x) + " y : " + str(pop[0].route[len(pop[0].route) - 1].y))

    print(len(pop))
    print(calcCost(pop[0]))

    flag = True
    count = 0
    prevMinCost = math.inf
    print(str(prevMinCost))
    while True:
        listOfCosts = list()
        count += 1
        avg = 0
        for i in pop:
            c = calcCost(i)
            avg += c
            listOfCosts.append(c)
        listOfCosts.sort(reverse=True)
        maxCostPerGen.append(listOfCosts[0])
        avgCostPerGen.append(avg / len(pop))
        pop = createNextGen(pop)
        print(str(count))
        if calcCost(pop[0]) < prevMinCost:
            prevMinCost = calcCost(pop[0])
            count = 0
        if count >= 5:
            flag = False
            break

    print('COUNT:' + str(count))
    print(len(pop))
    print(calcCost(pop[0]))
    # Print analytics information
    t1 = time.perf_counter()
    print("Run time: " + str(t1 - t0) + " seconds (" + str((t1 - t0)/60) + " minutes)")
    # Code for max cost / generation graph
    # plt.plot(maxCostPerGen)
    plt.plot(maxCostPerGen)
    plt.plot(avgCostPerGen)
    plt.ylabel('Cost($)')
    plt.xlabel('Generation')
    plt.legend(['Max Cost', 'Average Cost'], loc='upper left')
    plt.show()

    # Code for average cost / generation graph
    #plt.plot(avgCostPerGen)
    #plt.ylabel('Average Cost')
    #plt.xlabel('Generation')
    #plt.show


    #(1,1) | (2,1) | (3,2) | (3,3) | (4,2) | (4,3) | (4,4) |
if __name__ == "__main__":
    main()