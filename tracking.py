#!/usr/bin/python
import sys
from math import sqrt
from threading import Thread
from opencv.cv import *
from opencv.highgui import *
import Xlib
# Global Variables
#storage = cvCreateMemStorage(0)
#from Xlib import X,display,Xutil
storage=cvCreateMemStorage(0)
capture = cvCreateCameraCapture( 0 )

COLOR_RANGE={
'yellow': (cvScalar(10, 100, 100, 0), cvScalar(40, 255, 255, 0)),\
'red': (cvScalar(0, 0, 0, 0), cvScalar(190, 255, 255, 0)),\
'blue': (cvScalar( 90 , 84 , 69 , 0 ), cvScalar( 120 , 255 , 255 , 0)),\
'green': (cvScalar( 40 , 80 , 32 , 0), cvScalar( 70 , 255 , 255 , 0)),\
'orange': (cvScalar( 160 , 100 , 47 , 0 ), cvScalar( 179 , 255 , 255 , 0 ))\

}

DISPLAY_COLOR={
'yellow':CV_RGB(255,255,0)
,'red':CV_RGB(255,0,0)
,'blue':CV_RGB(0,0,255)
,'green':CV_RGB(0,110,0)

}


class Tracker(Thread):
   def __init__(self,color,flag):
      Thread.__init__(self)
      self.color=color
      self.display=DISPLAY_COLOR[color]
      self.path=cvCreateImage(cvSize(640,480),8,3)
      self.lastx=0
      self.lasty=0
      self.h_min=COLOR_RANGE[color][0]
      self.h_max=COLOR_RANGE[color][1]
      self.flag=flag
      if self.flag:
         cvNamedWindow(self.color,1) 
   
   def poll(self,img):
      if 1:
         thresh = cvCreateImage( cvSize(img.width,img.height), 8, 1 )
         new_img=cvCreateImage( cvSize(img.width,img.height),8 ,3 )
         cvCopy(img,new_img)
         cvCvtColor(img, new_img, CV_BGR2HSV )
         cvInRangeS(new_img,self.h_min,self.h_max,thresh)
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
            print self.color+ " Ball found at",x,y
            if self.lastx > 0 and self.lasty > 0:
               cvLine(self.path,cvPoint(self.lastx,self.lasty),cvPoint(x,y),self.display,5)
            self.lastx=x
            self.lasty=y
         cvAdd(img,self.path,img)
         if self.flag:
            cvShowImage(self.color,thresh)

         cvShowImage("result",img)
         if( cvWaitKey( 10 ) >= 0 ):
            return


if __name__ == '__main__':
   cvNamedWindow( "result", CV_WINDOW_AUTOSIZE )
   if capture:
      frame_copy = None
   yellow=Tracker("yellow",1)
   green=Tracker("green",1)
   blue=Tracker("blue",1)
   yellow.start()
   green.start()
   blue.start()
   while True:
      img=cvQueryFrame(capture)
      yellow.poll(img)
      green.poll(img)
      blue.poll(img)
      yellow.join()
      green.join()
      blue.join()
      if cvWaitKey(10) >=0:
         sys.exit(1)
   cvDestroyWindow("result")
 
