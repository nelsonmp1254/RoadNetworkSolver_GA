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
# Recommend altering either cxPartialyMatched, cxUniformPartialyMatched, or cxOrdered
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

creator.create('Individual', Path)


def main():
    # Node Generation
    width = 201
    height = 264
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

    print(grid[262][200].x)
    print(grid[262][200].y)
    print(grid[262][200].prevDir)
    print(grid[262][200].height)  # last node
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
    endNode = grid[99][99] # second city here
    
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
            if lastNode.x + xoffset < 100 and lastNode.x + xoffset > 0:
                if lastNode.y + yoffset < 100 and lastNode.y + yoffset > 0:
                    nodeToAdd = grid[lastNode.x + xoffset][lastNode.y + yoffset]
                    lastNode = nodeToAdd
                    startingPath.append(nodeToAdd)

        pop.append(Path(startingPath))


    print(len(pop))
    for i in range(len(pop)):
        print(pop[i].route[len(pop[i].route) - 1].toString())





if __name__ == "__main__":
    main()