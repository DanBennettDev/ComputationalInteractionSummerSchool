import cv2
import numpy as np
import math
import pickle
import time

class DrawingWindow(object):
#     drawing = False # true if mouse is pressed
#     ix,iy   
#     linebuffer
#     allLines
#     img
    
    def __init__(self):
        self.ix,self.iy = -1,-1
        self.linebuffer =[]
        self.allLines= []
        self.img = np.zeros((512,512,4), np.uint8)
        cv2.namedWindow('image')
        self.drawing = False
        self.newData = False 
        self.closed = False
        

        
    def setup(self):
        cv2.setMouseCallback('image',self.mouseActions)
        
    def getAllData(self):
        return np.array(self.allLines)

    def getLatestData(self):
        self.newData = False
        return np.array(self.linebuffer)
    
    # mouse callback function
    def mouseActions(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix,self.iy = x,y
            self.linebuffer = []
            self.linebuffer.append((x,y))
            # start logging

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv2.circle(self.img,(x,y),5,(0,0,255),-1)
                self.linebuffer.append(np.array([x,y]))

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.circle(self.img,(x,y),5,(0,0,255),-1)
            self.allLines.append(np.array(self.linebuffer))
            # clear the window
            self.img = np.zeros((512,512,4), np.uint8)
            self.newData = True
    

    def draw(self):
        if self.closed == True:
            cv2.destroyAllWindows()
            return -1
        else:
            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                self.closed = True
                cv2.destroyAllWindows()
                return -1
            elif self.newData == True:
                return 1
            return 0
        
    def displayImg(self, img, x, y):
        self.img[y:y+img.shape[0], x:x+img.shape[1]] = img

    def clear(self):
        self.img = np.zeros((512,512,4), np.uint8)
        
    def close(self):
        self.closed = True
        cv2.destroyAllWindows()


    