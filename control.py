import socket
import sys

ip = "192.168.2.1"
port = 40923

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def createConnection():

    address = (ip, int(port))
    print("Connecting...")
    s.connect(address)
    print("Connected!")

def closeConnection():      
    s.shutdown(socket.SHUT_WR)
    s.close()
    print("Disconnected")

def move_cmd(x, y, z):
    x = str(x)
    y = str(y)
    z = str(z)

    return "chassis move x " + x + " y " + y + " z " + z + ";"

def change_wheel(w1, w2, w3, w4):
    w1 = str(w1)
    w2 = str(w2)
    w3 = str(w3)
    w4 = str(w4)
    return "chassis wheel w1 " + w1 + " w2 " + w2 + " w3 " + w3 +  + " w4 " + w4 + ";"


def controll(cmd, an=0):
    
    if cmd.upper() == 'W':
        cmd = move_cmd(1.7, 0.0, 0.0)
    elif cmd.upper() == 'A':
        cmd = move_cmd(0.0, 0.0, -an)
    elif cmd.upper() == 'D':
        cmd = move_cmd(0.0, 0.0, an)
    elif cmd.upper() == 'S':
        cmd = move_cmd(-1.7, 0.0, 0.0)
    elif cmd.upper() == 'L':
        cmd = move_cmd(0.0, -0.3, 0.0)
    elif cmd.upper() == 'R':
        cmd = move_cmd(0.0, 0.3, 0.0)
    elif cmd.upper() == 'F':
        cmd = move_cmd(3.5, 0.0, 0.0)
    
    if cmd.upper() == 'Q':
        sys.exit(1)
    
    s.send(cmd.encode('utf-8'))

    try:    
        buf = s.recv(1024)  
        print(buf.decode('utf-8'))
        

    except socket.error as e:
        print("Error receiving :", e)
        sys.exit(1)
    if not len(buf):
        sys.exit(1)
