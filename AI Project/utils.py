
#  Several helpful tools for traversing 2D square grids

DIRECTIONS = "NESW"
ORIENTATIONS = dict(N=(0,1), E=(1,0), S=(0,-1), W=(-1,0))

def next_move(d, inc):
    return DIRECTIONS[(DIRECTIONS.index(d)+inc) % len(DIRECTIONS)]

def move_left(d):
    return next_move(d, -1)

def move_right(d):
    return next_move(d, 1)

def next_location(loc, d):
    x,y = loc
    dx, dy = ORIENTATIONS[d]
    return (x+dx, y+dy)

def valid_location(loc, n):
    x,y = loc
    return 0<=x<n and 0<=y<n

def locations(n):
    for x in range(n):
        for y in range(n):
            yield (x,y)

def manhatDist(loc1, loc2):
    x1,y1 = loc1
    x2,y2 = loc2
    return abs(x1-x2) + abs(y1-y2)

def adjacent(l1,l2):
    x1,y1 = l1
    x2,y2 = l2
    return (abs(x1-x2) + abs(y2-y1)) == 1

