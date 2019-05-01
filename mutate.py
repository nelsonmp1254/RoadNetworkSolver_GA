def mutate(p1, mutateFactor = 0.2):
    for x in range(1, len(p1) - 1):
        if (random.randint(1, 10) < (mutateFactor * 10)):
            
            if(x - 1 >= 0 and x + 1 <= 49) and \
                    ((p1[x].prevDir == Direction.TOP and p1[x + 1].prevDir == Direction.TOP) or \
                    (p1[x].prevDir == Direction.BOTTOM and p1[x+1].prevDir == Direction.BOTTOM)):
                flag = random.randint(0, 1)
                if(flag == 1):
                    newNode = grid[p1[x].y][p1[x].x + 1]
                else:
                    newNode = grid[p1[x].y][p1[x].x - 1]
                
            cost = calcWeights(p1[x - 1], p1[x]) + calcWeights(p1[x], p1[x + 1])
            newCost = calcWeights(p1[x-1], newNode) + calcWeights(p1[x], newNode)
            
            if newCost < cost:
                p1[x] = newNode

