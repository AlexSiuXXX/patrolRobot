from rrt import runRRT, t
from util import dir_oriented, dist
from ostacle import flow
import time
from control import controll, createConnection, closeConnection
import argparse
import threading
import math

act = []

def start_loc(a, b):
    tr = math.atan2(((b[0]-a[0]), (b[1]-a[1])))
    return math.degrees(tr)

def genPath(args):
    runRRT(args)
    print(t)

    print('pathL ')
    dir_oriented(t, act)
   
    for i in range(len(t)*2):
        if i % 2 != 0:
            act.insert(i, ('forward', 0.0))

    for i, j in enumerate(act):
        print(i, j)


def cont():
    createConnection()
    
    msr = 'command;'
    controll(msr, 0)

    for i in range(1, len(act)):
        if (act[i][0] == 'forward'):
            print('forward', act[i][1])
            controll('w')
            time.sleep(5)
        elif (act[i][0] == 'right' and act[i][1] > 25.0):
            print('right', act[i][1])
            controll('d', act[i][1])
            time.sleep(5)
        elif (act[i][0] == 'left' and act[i][1] > 25.0):
            print('left', act[i][1])
            controll('a', act[i][1])
            time.sleep(5)
    
    controll('f')
    
    closeConnection()
    



if __name__=='__main__':

    parser = argparse.ArgumentParser(description = 'Below are the params:')
    parser.add_argument('-p', type=str, default='world2.png',metavar='ImagePath', action='store', dest='imagePath',
                    help='Path of the image containing mazes')
    parser.add_argument('-s', type=int, default=10,metavar='Stepsize', action='store', dest='stepSize',
                    help='Step-size to be used for RRT branches')
    parser.add_argument('-start', type=int, default=[20,20], metavar='startCoord', dest='start', nargs='+',
                    help='Starting position in the maze')
    parser.add_argument('-stop', type=int, default=[450,250], metavar='stopCoord', dest='stop', nargs='+',
                    help='End position in the maze')
    parser.add_argument('-selectPoint', help='Select start and end points from figure', action='store_true')

    args = parser.parse_args()

    p = threading.Thread(target=genPath, args=(args,))
    p.start()
    p.join()
    
    gp = threading.Thread(target=flow)
    gp.start()
    
    ct = threading.Thread(target=cont)
    ct.start()




    

    
    

    




    
    

