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
    grade = abs(node1.height - node2.height)
    xdiff = abs(node1.x - node2.x) * dataPointOffset
    ydiff = abs(node1.y - node2.y) * dataPointOffset
    dist = (xdiff)**2 + (ydiff)**2
    dist = math.sqrt(dist)
    grade = (grade / dist) * 100 # grade as percentage

    sum = dist * distWeight + grade * inclWeight

    # difference in road angles: higher = less direct route
    curve = abs(node1.prevDir - node2.prevDir) % 360
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