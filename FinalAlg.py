# import necessary dependencies
from deap import base
from deap import creator
from deap import tools
from enum import Enum
import csv
import random
import numpy

grid = None

# register operators & create toolbox
toolbox = base.Toolbox()
#toolbox.register('crossover', PICK_A_CROSSOVER_FUNCTION)
#Recommend altering either cxPartialyMatched, cxUniformPartialyMatched, or cxOrdered
#toolbox.register('mutate', PICK_A_MUTATION_FUNCTION)
#toolbox.register('select', SELECT_INDIVIDUALS_TO_BREED)

# create a lovely enum to hold directions in
class Direction(Enum):
    TOP = 90,
    TOP_RIGHT = 45,
    RIGHT = 0,
    BOTTOM_RIGHT = 315,
    BOTTOM = 270,
    BOTTOM_LEFT = 225,
    LEFT = 180,
    TOP_LEFT = 135


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


def createAdjMatrix(grid):

    cols = len(grid[0])
    rows = len(grid)

    matrix = [ [0]* (cols * rows) for _ in range(rows * cols)]

    for i in range(rows):
        for j in range(cols):       # Replace 1s with cost of travel between node [j][i] and [j +- 1/0][i +- 1/0]
            if i - 1 > 0:
                matrix[j][i - 1] = 1
                if j - 1 > 0:
                    matrix[j - 1][i - 1] = 1
            if i + 1 < 200:
                matrix[j][i + 1] = 1
                if j + 1 < 200:
                    matrix[j + 1][i + 1] = 1
            if j - 1 > 0:
                matrix[j - 1][i] = 1
            if j + 1 < 263:
                matrix[j + 1][i] = 1
    matrix[263][200] = 10
    #print(len(matrix))


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


def shortestPath(p1, p2):
    return 10


def connectPaths(p1, n, p2):

    listA = p1[len(p1) - 3 : len(p1)]
    listB = p2[0 : 3]

    min = 10000000.0
    for x in listA:
        cost = 10
        aConnect = shorestPath(x,n)


    for x in listB:
        bConnect = shortestPath(x,n)

    return p1.append(aConnect).appent(n).append(bConnect).append(p2)

def cleanup(p1):

    i = 0
    while True:
        if(i >= len(p1)):
            break
        for j in range(len(p1)):
            for h in reversed(range(len(p1) - 1, 0, -1)):
                if p1[h] == p1[j] and j != h:
                    p1 = p1[:j] + p1[h:]
                    print("h : " + str(h) + ", i : " + str(i) + ", j : " + str(j))
                    break
            break
        i += 1
    return p1




def mutate(p1):
    mutateFactor = 0.2
    min = 1000000000.0
    for x in range(len(p1)):
        if (random.randint(1, 10) < (mutateFactor * 10)):
            cost = 10       # replace with cost fn
            if cost < min:
                return cost


creator.create('Individual', Path)


def main():
    # Node Generation
    width = 50
    height = 50
    blank = Node(0, 0, 0, 0)
    grid = [[blank for x in range(width)] for y in range(height)]
    with open("C:\\Users\\nelsonmp\\testInput.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        d = list(reader)

    i = 0  # height / y
    # print(d[9][11])
    for k in d:
        l = 0  # width / x
        for j in k:
            grid[i][l] = Node(i, l, d[i][l], Direction.RIGHT)
            l += 1
        i += 1

    print(grid[49][49].x)
    print(grid[49][49].y)
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
                    nodeToAdd = grid[lastNode.x + xoffset][lastNode.y + yoffset]
                    lastNode = nodeToAdd
                    startingPath.append(nodeToAdd)
        pop.append(Path(startingPath))
        startingPath = []




    print(len(pop[0].route))
    pop[0] = Path(cleanup(pop[0].route))
    print(len(pop[0].route))
    print("x : " + str(pop[0].route[len(pop[0].route) - 1].x) + " y : " + str(pop[0].route[len(pop[0].route) - 1].y))
    print(pop[0].printPath())




if __name__ == "__main__":
    main()