# import necessary dependencies
from enum import Enum
import csv
import random
import matplotlib.pyplot as plt
import math
import time


# create Node class - X, Y, Height
class Node:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

#Reads in a text file of data (fakeElevationData.txt) and inserts this into a Rectangular Array of Nodes
#These nodes are then used in a random walk algorithm for travel from point A to point B
width = 10
height = 10
blank = Node(0,0,0)
grid = []
grid = [[blank for x in range(width)] for y in range(height)]
with open("fakeElevationData.txt") as file:
    reader = csv.reader(file, delimiter="\t")
    d = list(reader)
i = 0  # height / y
for k in d:
    l = 0  # width / x
    for j in k:
        grid[i][l] = Node(l, i, d[i][l])
        l += 1
    i += 1
midNode = grid[5][5]
endNode = grid[9][9]

# create custom Individual class. Wrapper for a 'route', or a list of paths
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

#Checks if a path contains a node. Returns true or false
def contains(path, node = grid[5][5]):
    for x in path:
        if x == node:
            return True
    return False

def cleanup(p1, midNode = grid[5][5], endNode = grid[9][9]):
    i = 0
    while i < len(p1):
        for j in range(len(p1)):
            for h in reversed(range(len(p1) - 1, 0, -1)):
                if j < h and j < len(p1) and h < len(p1) and p1[h] == p1[j] and j != h:

                    newPath = p1[:j] + p1[h:]
                    if contains(newPath, midNode) and contains(newPath, endNode):
                        i = 0
                        p1 = newPath
                        break
                    #p1 = p1[:j] + p1[h:]
        i += 1
    return p1

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

#Returns a string containing all the nodes in a path, formatted for readability
def pathPrinter(p1):
    ret = ""
    for i in p1.route:
        ret += grid[i.y][i.x].toString() + " | "
    return ret


# Cleans up random walk. Eliminates loops. Variable effectiveness depending on the random walk


#Finds the change in direction between two nodes
def prevDir(n1, n2):
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
def breed(p1, p2, midNode = grid[5][5], endNode = grid[9][9]):
    child1 = list()
    child2 = list()
    parent1 = p1.route
    parent2 = p2.route
    crosspt = pathsCross(p1, p2)
    if crosspt != (-1, -1):
        child1 = parent1[:crosspt[0]] + parent2[crosspt[1]:]
        child2 = parent2[:crosspt[1]] + parent1[crosspt[0]:]
    if contains(child1, midNode) and contains(child1, endNode) and contains(child2, midNode) and contains(child2, endNode) :
        return Path(child1), Path(child2)
    else:
        return -1, -1

#Iterates through a path, has a random chance to 'mutate' each node.
#Defaults currently to 10% per node
#Each mutate has a chance to replace a node in the path with an adjacent node.
#Least optimized portion of algorithm
def mutate(p1, mutateFactor=0.1, midNode = grid[5][5]):
    for x in range(len(p1) - 1 ):
        if random.randint(1, 10) <= (mutateFactor * 10) and x - 1 > 0 and x + 1 < 10 and p1[x] != midNode:
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
            if p1[x].x + xoffset > 1 and p1[x].x + xoffset < 10 and \
                    p1[x].y + yoffset > 1 and p1[x].y + yoffset < 10 and \
                    x - 1 > 0 and x + 1 < 10:

                newCost = calcWeights(p1[x - 1], grid[p1[x].y + yoffset][p1[x].x + xoffset], p1[x + 1])
                if newCost < cost:
                    p1[x] = grid[p1[x].y + yoffset][p1[x].x + xoffset]

#Calculate the cost of the full path
def calcCost(path):
    cost = 0
    cost += calcWeights(path.route[1], path.route[0], path.route[0])
    for i in range(2, len(path.route)): #cost += calcWeights(path.route[i], path.route[i], path.route[i])
        cost += calcWeights(path.route[i], path.route[i - 1], path.route[i-2])
    return cost

#Sorts paths when given a list of paths (pop)
def sortPaths(paths):
    for i in range(len(paths)):
        for j in range(0, len(paths)-i-1):
            if calcCost(paths[j]) > calcCost(paths[j+1]):
                paths[j], paths[j + 1] = paths[j + 1], paths[j]
    return paths

#Sorts the paths, and then returns a list containing the X lowest cost paths. Defualts to 20
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
#Creates a list of new paths from a list of paths.
#Mutates, then breeds, then culls the paths, returning a list of the same size.
#Breeding makes all possible combinations of paths (ie. every crossing point)
#Ideally, and with the test sample size, this ensures that no 'genetic diversity' is lost
def createNextGen(paths):
    for i in range(len(paths)):
        path = Path(paths[i].route)
        mutate(path.route)             #Mutates Path
    n = len(paths)
    for j in range(n):                         #Breeds Paths
        for k in range(n) :
            if(paths[j] is not None and paths[k] is not None):
                breedingPath1 = paths[j]
                breedingPath2 = paths[k]
                newPath1 = Path([])
                newPath2 = Path([])
                if (isinstance(breedingPath1, Path) and isinstance(breedingPath2, Path)):
                    newPath1, newPath2 = breed(breedingPath1, breedingPath2)
                if(newPath1 != -1):
                    paths.append(Path(newPath1.route))
                    paths.append(Path(newPath2.route))
    for h in range(len(paths)):                         #cleanup
        paths[h] = Path(cleanup(paths[h].route))

    paths = cull(paths, 20)
    return paths


#The random walk paths are cleaned up and sorted to display the shortest cost path
#Then we generate new populations until the cost no longer changes, giving us our best path
#Takes approximately 5 minutes to run in our worst case seen (Randomness makes this hard to guarantee).
def main():
    t0 = time.perf_counter()
    # Keep track of fitness metrics for each generation
    maxCostPerGen = list()
    avgCostPerGen = list()
    crossProb   = 0.2
    mutProb     = 0.2
    generations = 0
    pop         = list()
    startPop    = 20  # starting population size

    startNode = grid[0][0]  # fist city here
    midNode   = grid[5][5]  # mid city here
    endNode   = grid[9][9]  # end city here

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
    startingPath.append(grid[0][0])
    for i in range(startPop):
        lastNode   = startNode
        startNode  = grid[0][0]  # fist city here
        midNode    = grid[5][5]    # middle city here
        endNode    = grid[9][9]    # third city here
        nodeToAdd  = None
       # random.seed( 30 )
        endFlag = True
        midFlag = True
        while endFlag or midFlag:
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
                    if nodeToAdd == midNode:
                        midFlag = False
                    if nodeToAdd == endNode:
                        endFlag = False
                    lastNode = nodeToAdd
                    startingPath.append(nodeToAdd)
        endFlag = True
        midFlag = True
        pop.append(Path(startingPath))
        startingPath = []

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
    print("Run time: " + str(t1 - t0) + " seconds (" + str((t1 - t0) / 60) + " minutes)")
    # Code for max cost / generation graph
    # plt.plot(maxCostPerGen)
    plt.plot(maxCostPerGen)
    plt.plot(avgCostPerGen)
    plt.ylabel('Cost($)')
    plt.xlabel('Generation')
    plt.legend(['Max Cost', 'Average Cost'], loc='upper left')
    plt.show()

    # Code for average cost / generation graph
    # plt.plot(avgCostPerGen)
    # plt.ylabel('Average Cost')
    # plt.xlabel('Generation')
    # plt.show


if __name__ == "__main__":
    main()
