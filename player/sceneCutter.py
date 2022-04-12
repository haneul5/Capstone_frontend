import cv2
from cv2 import FORMATTER_FMT_NUMPY 
import numpy as np
import os

cap = cv2.VideoCapture('./video/news.mp4')    # 비디오 경로 수정 필요
totalFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))    # 초당 프레임 수 
# print("fps: " ,fps) 

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 프레임 너비
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # 프레임 높이

imgName = []
videoTime = []

def getImage():
    frameNum = -1
    psnrV = 0 
    CHANGE_DETECT_AUDIO = 15.0
    
    prevFrame = np.zeros((height,width,3), np.uint8)
    currFrame = np.zeros((height,width,3), np.uint8)
    changeFrame =np.zeros((height,width,3), np.uint8)
    
    while(cap.isOpened()):
        frameNum+=1
        ret, img = cap.read(currFrame)
        
        if frameNum < 1:
            prevFrame = currFrame.copy()
            changeFrame = currFrame.copy()
            saveImage(currFrame,0)
            continue
        
        if (frameNum % fps == 0) :
            
            if not ret: break
            
            
            print("total : ", totalFrameNum , "frameNum : ", frameNum)
            psnrV = getPSNP(prevFrame, currFrame)
            # print("psnrV: ",psnrV)
            
            if psnrV < CHANGE_DETECT_AUDIO:
                changeFrame = currFrame.copy()
                saveImage(changeFrame, frameNum / fps)
                
            prevFrame = currFrame.copy()
            
            
def saveImage(res, sec):
    path = "media/frame%d.jpg" % sec  # 이미지 저장 경로 변경 필요
    imgName.append(path)
    videoTime.append(sec)
    cv2.imwrite(path, res)


def getPSNP(I1, I2):
    s1 = np.zeros((I1.shape[0],I2.shape[1],3), np.uint8)
    
    diff = cv2.absdiff(I1,I2,s1)
    s1 = np.float32(s1)
    s1 = cv2.multiply(s1,s1)
    
    s1_h = s1.shape[0]
    s1_w = s1.shape[1]
    s1_bpp = s1.shape[2]
    
    s=cv2.sumElems(s1)
    ## i dont know...
    sse = s[0] + s[1] +s[2]
    print("sse : ",sse)
    
    if sse <= 1e-10 :
        return 0
    
    mse = sse / np.double(3 * width * height)
    psnr = 10.0 * np.log10((255*255)/mse)
    
    return psnr

getImage()