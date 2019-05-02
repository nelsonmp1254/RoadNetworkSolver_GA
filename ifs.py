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
     or (pDir == Direction.BOTTOM_LEFT and cDir == Direction.TOP_LEF):
yoffset = -1
xoffset = 0
# CASE
# __
#  /
elif (pDir == Direction.RIGHT and cDir == Direction.BOTTOM_LEF) \
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