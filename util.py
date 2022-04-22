import math


class point:
    def __init__(self):
        self.x = 0
        self.y = 0
   
# Constant integers for directions
RIGHT = 1
LEFT = -1
ZERO = 0

def dist(a, b):
    ta = (a[0]+b[0])**2
    tb = (a[1]+b[1])**2
    return math.sqrt(ta+tb)

def directionOfPoint(A, B, P):
      
    global RIGHT, LEFT, ZERO
      
    # Subtracting co-ordinates of 
    # point A from B and P, to 
    # make A as origin
    B.x -= A.x
    B.y -= A.y
    P.x -= A.x
    P.y -= A.y
   
    cros_prod = B.x * P.y - B.y * P.x
   
    # Return RIGHT if cross product is positive
    if (cros_prod > 0):
        return RIGHT     
    # Return LEFT if cross product is negative
    if (cros_prod < 0):
        return LEFT
   
    return ZERO

def vatorize(a, b):
    return (b[0]-a[0], b[1]-a[1])

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def normalize(a):
    return math.sqrt(a[0]**2+a[1]**2)


def start_loc(a, b):
    tr = math.atan2((b[0]-a[0]), (b[1]-a[1]))
    return math.degrees(tr)


def dir_oriented(t, act):
    

    A = point()
    B = point()
    P = point()

    st_ang = start_loc(t[0], t[1])
    print("starter angle", st_ang)

    if (st_ang < 0):
        act.append(('right', abs(st_ang)))
    else:
        act.append(('left', abs(st_ang)))
    
    # h, l = img.shape
    for i, j in enumerate(t):
        if (i < len(t) - 2):
            print(t[i][0], t[i][1], t[i+1][0], t[i+1][1], t[i+2][0], t[i+2][1])
            print('\n')
            A.x = t[i][0]
            A.y = t[i][1]
            B.x = t[i+1][0]
            B.y = t[i+1][1]
            P.x = t[i+2][0]
            P.y = t[i+2][1]
            direction = directionOfPoint(A, B, P)

            va = vatorize(t[i], t[i+1])
            vb = vatorize(t[i+1], t[i+2])

            d = dist(t[i], t[i+1])

            dott = dot(va, vb)
            nora = normalize(va)
            norb = normalize(vb)

            angle = math.acos(dott/(nora*norb))
            
           
            if (direction == 1):
                print("Right Direction", math.degrees(angle))
                act.append(('right', math.degrees(angle)))
            elif (direction == -1):
                print("Left Direction", math.degrees(angle))
                act.append(('left', math.degrees(angle)))
            else:
                print("Point is on the Line")



