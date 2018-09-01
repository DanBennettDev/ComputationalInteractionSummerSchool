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
        self.newClick = False
        self.lastClick = [0, 0]


        
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
            # distinguish between click and draw
            if len(self.linebuffer) > 10:
                self.allLines.append(np.array(self.linebuffer))
                self.newData = True
            else:
                self.lastClick = [x, y]
                self.newClick = True
            # clear the window
            self.img = np.zeros((512,512,4), np.uint8)
    

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
        
        
        
    def displayImg(self, overlay, x, y, scale=1):
#         self.img[y:y+overlay.shape[0], x:x+overlay.shape[1]] = overlay
        
        
        overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
        h,w,_ = overlay.shape  # Size of foreground
        rows,cols,_ = self.img.shape  # Size of background Image
#         y,x = pos[0],pos[1]    # Position of foreground/overlay image

        #loop over all pixels and apply the blending equation
        for i in range(h):
            for j in range(w):
                if x+i >= rows or y+j >= cols:
                    continue
                alpha = float(overlay[i][j][3]/255.0) # read the alpha channel 
                self.img[x+i][y+j][:3] = alpha*overlay[i][j][:3]+(1-alpha)*self.img[x+i][y+j][:3]


    def getClick(self):
        retNewClick = self.newClick
        self.newClick = False
        return self.lastClick, retNewClick

    def clear(self):
        self.img = np.zeros((512,512,4), np.uint8)
        
    def close(self):
        self.closed = True
        cv2.destroyAllWindows()


    