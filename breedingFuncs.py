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