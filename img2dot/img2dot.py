import sys
import cv2
import numpy as np
import pyperclip as pc

def trans(img,newSize):
    global dotMap
    dotMap = ''
    (newH,newW) = newSize
    for h in range(0,newH-1,4):
        for w in range(0,newW-1,2):
            index = 0
            for i in range(2):
                for j in range(4):
                    index += (2**(j+4*i))*img[h+j][w+i]
            dotMap += chr(10240+index)
        dotMap += '\n'

def threshold(img,thres):
    srcH,srcW = img.shape
    thresholdImg = np.zeros((srcH,srcW,1),dtype = "uint8")
    for i in range(srcH):
        for j in range(srcW):
            if img[i][j] >= thres:
                thresholdImg[i][j] = 1
            else:
                thresholdImg[i][j] = 0
    return thresholdImg

def linear(img,newSize):
   (srcH,srcW,c) = img.shape
   (newH,newW) = newSize
   img = np.pad(img,((0,1),(0,1),(0,0)),"constant")
   resizeImg = np.zeros((newH,newW,3),dtype = "uint8")
   for i in range(newH):
      for j in range(newW):
         x = (i+1)*(srcH/newH) - 1
         y = (j+1)*(srcW/newW) - 1
         Ix = int(x)
         Iy = int(y)
         a = x - Ix
         b = y - Iy
         resizeImg[i,j] = (1-a)*(1-b)*img[Ix,Iy]+a*(1-b)*img[Ix+1,Iy]+(1-a)*b*img[Ix,Iy+1]+a*b*img[Ix+1,Iy+1]
   return resizeImg

def main():
    global dotMap
    resize = (100,100)
    if(len(sys.argv) < 2):
        print("Usage: python3 dott.py imgPath\n")
        i = chr(10241)
        print(i)
        exit(1)
    thres = int(input("threshold(0~255) :"))
    path = sys.argv[1]
    img = cv2.imread(path,1)
    (srcH,srcW,c) = img.shape
    if srcH < srcW:
        resize = (100,int((srcW/srcH)*100))
    else:
        resize = (int((srcH/srcW)*100),100)
    print(resize)
    img = linear(img,resize)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """for i in range(60):
        debug = ''
        for j in range(60):
            print("%3s" % str(img[i][j]),end = '')
        print(debug)"""
    while thres != '':
        result = threshold(img,thres)
        trans(result,resize)
        print(dotMap)
        pc.copy(dotMap)
        thres = int(input("threshold(0~255) :"))

main()
input()