# TODO: Implement more efficient monotonic heuristic
#
# Every function receive coordinates of two grid points returns estimated distance between them.
# Each argument is a tuple of two or three integer coordinates.
# See file task.md for description of all grids.

import math

#Manhattan heuristic for grid
def grid_2D_heuristic(current, destination):
    return abs(destination[0]-current[0]) + abs(destination[1]-current[1])

#Max heuristic for grid with diagonals
def grid_diagonal_2D_heuristic(current, destination):
    return math.floor(max((destination[0]-current[0]),(destination[1]-current[1])))

#Manhattan heuristic for 3d grid
def grid_3D_heuristic(current, destination):
    return math.floor(abs(destination[0]-current[0]) + abs(destination[1]-current[1])) + abs(destination[2]-current[2])

#Heuristic for Face (combine Manhattan and the logic that you can only move up to 2 dimensions in one move)
def grid_face_diagonal_3D_heuristic(current, destination):
    dx = abs(destination[0]- current[0])
    dy = abs(destination[1] - current[1])
    dz = abs(destination[2] - current[2])
    dmin = min(dx, dy, dz)
    dmax = max(dx, dy, dz)
    dmid = dx + dy + dz - dmin - dmax
    
    
    if(dmax >= dmin + dmid):
        return dmax
    else:
        return math.ceil((dx + dy + dz)/2)
    
    

#Max heuristic for 3dGrid all diagonals
def grid_all_diagonal_3D_heuristic(current, destination):
    return max(abs(destination[0]-current[0]),abs(destination[1]-current[1]),abs(destination[2]-current[2]))
    

#If max and min distance are way too different, use aproximation for quadrants. Else use approximation of ("getting closer by 3 every turn")
def grid_knight_2D_heuristic(current, destination):
    dx = abs(destination[0]- current[0])
    dy = abs(destination[1] - current[1])
    dmin = min(dx, dy)
    dmax = max(dx, dy)
    
    if (math.floor(dmax/2) > dmin): 
        return math.floor(dmax/2)
    else:
        return math.ceil((dmax + dmin)/3)
   
