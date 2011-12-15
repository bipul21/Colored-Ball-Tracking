#!/usr/bin/python
import sys
from math import sqrt
from threading import Thread
from opencv.cv import *
from opencv.highgui import *
storage=cvCreateMemStorage(0)
capture = cvCreateCameraCapture( 0 )

COLOR_RANGE={
'yellow': (cvScalar(10, 100, 100, 0), cvScalar(40, 255, 255, 0)),\
'red': (cvScalar(10, 100, 100, 0), cvScalar(40, 255, 255, 0))\
}

DISPLAY_COLOR={'yellow':cvScalar(0,255,255)
,'red':cvScalar(255,0,0)}

def getImage():
   return cvQueryFrame( capture)

class Tracker(Thread):
   def __init__(self,color):
      Thread.__init__(self)
      self.color=color
      self.display=DISPLAY_COLOR[color]
      self.path=cvCreateImage(cvSize(640,480),8,3)

   def run(self):
      color=self.color
      cvNamedWindow(color,CV_WINDOW_AUTOSIZE)   
      h_min=COLOR_RANGE[color][0]
      h_max=COLOR_RANGE[color][1]
      lastx=0
      lasty=0
      while True:
         img = getImage()
         thresh = cvCreateImage( cvSize(img.width,img.height), 8, 1 )
         new_img=cvCreateImage( cvSize(img.width,img.height),8 ,3 )
         cvCopy(img,new_img)
         cvCvtColor(img, new_img, CV_BGR2HSV )
         cvInRangeS(new_img,h_min,h_max,thresh)
         cvSmooth(thresh,thresh,CV_GAUSSIAN,9,9)
         circles=cvHoughCircles(thresh,storage,CV_HOUGH_GRADIENT,2,thresh.height/4,200,100,25,0)
         maxRadius=0
         x=0
         y=0
         found=False
         for i in range(circles.total):
            circle=circles[i]
            if circle[2]>maxRadius:
               found=True
               radius=int(circle[2])
               maxRadius=int(radius)
               x=int(circle[0])
               y=int(circle[1])
         if found:
            cvCircle( img, cvPoint(x,y),3, CV_RGB(0,255,0), -1, 8, 0 )
            cvCircle( img, cvPoint(x,y),maxRadius, CV_RGB(255,0,0), 3, 8, 0 )
            print "Ball found at",x,y
            if lastx > 0 and lasty > 0:
               cvLine(self.path,cvPoint(lastx,lasty),cvPoint(x,y),self.display,5)
            lastx=x
            lasty=y
         cvAdd(img,self.path,img)
         cvShowImage(color,thresh)
         cvShowImage("result",img)
         if( cvWaitKey( 10 ) >= 0 ):
            break



if __name__ == '__main__':
   cvNamedWindow( "result", CV_WINDOW_AUTOSIZE )
   t=Tracker("yellow")
   t.start()
   cvDestroyWindow("result")

