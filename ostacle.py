import pyrealsense2 as rs
import numpy as np
import cv2
from control import controll
import time
import uuid




def flow():

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
    pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)

    uuidStr = uuid.uuid4().hex

    fileName = 'out_cam_' + uuidStr + '.avi'

    print(fileName)
    out = cv2.VideoWriter(fileName ,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))

    try:
        while True:
                                    
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)   
            depth_frame = aligned_frames.get_depth_frame() 
            color_frame = aligned_frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                continue

    
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
    
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_WINTER)


            text_depth = "depth value of point (320,280) is " + str(np.round(depth_frame.get_distance(320, 280), 4)) + "meter(s)"
            text_depth2 = "depth value of point (150,280) is " + str(np.round(depth_frame.get_distance(150, 280), 4)) + "meter(s)"
            text_depth3 = "depth value of point (500,280) is " + str(np.round(depth_frame.get_distance(500, 280), 4)) + "meter(s)"
       
            
            color_image = cv2.circle(color_image, (320,280), 2, (0,255,255), -1)
            color_image = cv2.circle(color_image, (150,280), 2, (0,255,255), -1)
            color_image = cv2.circle(color_image, (500,280), 2, (0,255,255), -1)
            color_image = cv2.putText(color_image, text_depth, (10, 20),  cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2, cv2.LINE_AA)
            color_image = cv2.putText(color_image, text_depth2, (10, 40),  cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2, cv2.LINE_AA)
            color_image = cv2.putText(color_image, text_depth3, (10, 60),  cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2, cv2.LINE_AA)
            
            disL = np.round(depth_frame.get_distance(320, 280), 4)
            disM = np.round(depth_frame.get_distance(150, 280), 4)
            disR = np.round(depth_frame.get_distance(500, 280), 4)
            
            if disL > 0.0 and disM > 0.0 and disR > 0.0:
                if disL < 0.53 and disM < 0.45 and disR < 0.53:
                    controll('s')
                    time.sleep(1)
                    controll('a', 35)
                    
                    
                
                elif disL < 0.53 and disM < 0.45:
                    print('right shift and turn right')
                    controll('r')
                    time.sleep(2)
                    controll('d', 20)
                    
                    
                elif disR < 0.53 and disM < 0.45:   
                    print('left shift and turn left', disR, disM)
                    controll('l')
                    time.sleep(2)
                    controll('a', 20)
                    
                    
                    
                elif disL < 0.5:
                    print('right shift and turn right', disL)
                    controll('r')
                    time.sleep(2)
                    controll('d', 20)
                    
                
                    
                elif disR < 0.5:
                    print('left shift and turn left', disR)
                    controll('l')
                    time.sleep(2)
                    controll('a', 20)
                    
                    

                elif disR < 0.5 and disL > disR and disM > disR:

                    print('left shift and turn left', disR)
                    controll('l')
                    time.sleep(1)
                    controll('a', 20)
                    
            
                elif disL < 0.5 and disR > disL and disM > disL:

                    print('right shift and turn right', disL)
                    controll('r')
                    time.sleep(1)
                    controll('d', 20)
                    
                    

                
            images = color_image
            
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            out.write(images)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

    finally:
        pipeline.stop()



            