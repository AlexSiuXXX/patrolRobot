

import math
import random
import cv2
import numpy as np

img2 = cv2.imread('result.png')
coordinates = []

t = []

class Nodes:
    """Class to store the RRT graph"""
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.parent_x = []
        self.parent_y = []

# check collision
def collision(x1, y1, x2, y2, img):
    color = []
    x = list(np.arange(x1,x2,(x2-x1)/100))
    y = list(((y2-y1)/(x2-x1))*(x-x1) + y1)
    print("collision",x,y)
    for i in range(len(x)):
        print(int(x[i]),int(y[i]))
        color.append(img[int(y[i]),int(x[i])])
    if (0 in color):
        return True #collision
    else:
        return False #no-collision

# check the  collision with obstacle and trim
def check_collision(x1, y1, x2, y2, img, stepSize, end):
    _,theta = dist_and_angle(x2,y2,x1,y1)
    x=x2 + stepSize*np.cos(theta)
    y=y2 + stepSize*np.sin(theta)
    print(x2, y2, x1, y1)
    print("theta", theta)
    print("check_collision", x, y)

    
    hy, hx = img.shape
    if y < 0 or y > hy or  x < 0 or x > hx:
        print("Point out of image bound")
        directCon = False
        nodeCon = False
    else:
        # check direct connection
        if collision(x, y, end[0], end[1], img):
            directCon = False
        else:
            directCon=True

        # check connection between two nodes
        if collision(x, y, x2, y2, img):
            nodeCon = False
        else:
            nodeCon = True

    return(x,y,directCon,nodeCon)


def dist_and_angle(x1, y1, x2, y2):
    dist = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
    angle = math.atan2(y2-y1, x2-x1)
    return(dist, angle)


def nearest_node(x, y, node_list):
    temp_dist=[]
    for i in range(len(node_list)):
        dist,_ = dist_and_angle(x, y, node_list[i].x, node_list[i].y)
        temp_dist.append(dist)
    return temp_dist.index(min(temp_dist))


def rnd_point(h, l):
    new_y = random.randint(0, h)
    new_x = random.randint(0, l)
    return (new_x, new_y)


def RRT(img, start, end, stepSize, node_list):
    h,l= img.shape # dim of the loaded image
    # print(img.shape) # (384, 683)
    # print(h,l)

    # node_list = [0] # list to store all the node points         
    node_list[0] = Nodes(start[0],start[1])
    node_list[0].parent_x.append(start[0])
    node_list[0].parent_y.append(start[1])

    
    cv2.circle(img2, (start[0],start[1]), 5, (0,0,255), thickness=3, lineType=8)
    cv2.circle(img2, (end[0],end[1]), 5, (0,0,255), thickness=3, lineType=8)

    i=1
    pathFound = False
    while pathFound == False:
        nx,ny = rnd_point(h,l)
        print("Random points:",nx,ny)

        nearest_ind = nearest_node(nx,ny, node_list)
        nearest_x = node_list[nearest_ind].x
        nearest_y = node_list[nearest_ind].y
        print("Nearest node coordinates:", nearest_x, nearest_y)

        #check direct connection
        tx, ty, directCon, nodeCon = check_collision(nx, ny, nearest_x, nearest_y, img, stepSize, end)
        print("Check collision:",tx, ty, directCon, nodeCon)

        if directCon and nodeCon:
            print("Node can connect directly with end")
            node_list.append(i)
            node_list[i] = Nodes(tx,ty)
            node_list[i].parent_x = node_list[nearest_ind].parent_x.copy()
            node_list[i].parent_y = node_list[nearest_ind].parent_y.copy()
            node_list[i].parent_x.append(tx)
            node_list[i].parent_y.append(ty)

            cv2.circle(img2, (int(tx), int(ty)), 2, (0,0,255), thickness=3, lineType=8)
            cv2.line(img2, (int(tx),int(ty)), (int(node_list[nearest_ind].x), int(node_list[nearest_ind].y)), (0,255,0), thickness=1, lineType=8)
            cv2.line(img2, (int(tx),int(ty)), (end[0], end[1]), (255,0,0), thickness=2, lineType=8)

            print("Path has been found")

            t.append(start)
            #print("parent_x",node_list[i].parent_x)
            for j in range(1, len(node_list[i].parent_x)-1):
                cv2.line(img2, (int(node_list[i].parent_x[j]),int(node_list[i].parent_y[j])), (int(node_list[i].parent_x[j+1]), int(node_list[i].parent_y[j+1])), (255,0,0), thickness=2, lineType=8)
                cx = node_list[i].parent_x[j]
                cy = node_list[i].parent_y[j]
                t.append((cx, cy))
            
            t.append(end)
            # cv2.waitKey(1)
            cv2.imwrite("media/"+str(i)+".jpg",img2)
            cv2.imwrite("out.jpg",img2)
            break

        elif nodeCon:
            print("Nodes connected")
            node_list.append(i)
            node_list[i] = Nodes(tx,ty)
            node_list[i].parent_x = node_list[nearest_ind].parent_x.copy()
            node_list[i].parent_y = node_list[nearest_ind].parent_y.copy()
            # print(i)
            # print(node_list[nearest_ind].parent_y)
            node_list[i].parent_x.append(tx)
            node_list[i].parent_y.append(ty)
            i=i+1
            
            
            cv2.circle(img2, (int(tx),int(ty)), 2,(0,0,255),thickness=3, lineType=8)
            cv2.line(img2, (int(tx),int(ty)), (int(node_list[nearest_ind].x),int(node_list[nearest_ind].y)), (0,255,0), thickness=1, lineType=8)
            cv2.imwrite("media/"+str(i)+".jpg",img2)
            cv2.imshow("sdc",img2)
            cv2.waitKey(1)
            continue

        else:
            print("No direct con. and no node con. :( Generating new rnd numbers")
            continue

def draw_circle(event, x, y, flags, praram):
    global coordinates
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img2 ,(x,y),5,(255,0,0),-1)
        coordinates.append(x)
        coordinates.append(y)

def runRRT(args):
    
    
    img = cv2.imread(args.imagePath,0) # load grayscale maze image
    
    start = tuple(args.start) 
    end = tuple(args.stop) 
    stepSize = args.stepSize 
    node_list = [0]
    
    if args.selectPoint:
        print("Select start and end points by double clicking, press 'escape' to exit")
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw_circle)
        while(1):
            cv2.imshow('image',img2)
            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                break
        # print(coordinates)
        start=(coordinates[0],coordinates[1])
        end=(coordinates[2],coordinates[3])


    RRT(img, start, end, stepSize, node_list)





   