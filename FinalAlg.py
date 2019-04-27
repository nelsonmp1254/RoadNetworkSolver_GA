# import necessary dependencies
from deap import base
from deap import creator
from deap import tools
from enum import Enum

grid = None

# register operators & create toolbox
toolbox = base.Toolbox()
toolbox.register('crossover', PICK_A_CROSSOVER_FUNCTION)
toolbox.register('mutate', PICK_A_MUTATION_FUNCTION)
toolbox.register('select', SELECT_INDIVIDUALS_TO_BREED)

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


# create custom Individual class
class Path:
    # takes as args a list of Nodes
    def __init__(self, route):
        self.route = route

    def addToPath(self, n):
        self.route.append(n)





creator.create('Individual', Path)


def main():

    # read in data from file,
    # store data in 'graph'
    # Create starting population of paths via random walk
    # Mutate paths
    # Breeding (and culling) stage
    # Profit
    crossProb = 0.2
    mutProb = 0.2
    generations = 0

    # open & read file data
    filename = input("Enter the name of your data file")
    inFile = open(filename, "r")
    # CODE FOR FILE READING HERE

    # these are vars for dimensions of our array:
    # put actual data here after reading data in from file
    width = None
    height = None
    blank = Node({})
    grid = [[blank for x in range(width)] for y in range(height)]

    # now for the randomwalk






if __name__ == "__main__":
    main()