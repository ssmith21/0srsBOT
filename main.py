import cv2 as cv
import numpy as np
from random import shuffle
import time
from windowcapture import WindowCapture
from vision import Vision
from movement import *
from hsvfilter import HsvFilter
import concurrent.futures
import threading
from multiprocessing import Process, RLock
from multiprocessing.sharedctypes import Array
from ctypes import Structure, c_int
import pyautogui as pog

wincap = WindowCapture('Runelite - USERNAME')


item_1 = Vision('whirlpool.png')
item_2 = Vision('inventory.png')

class Point(Structure):
    _fields_ = [('x', c_int), ('y', c_int)]
lock = RLock()
A = Array(Point , 10 , lock=lock)  # Global shared Array

def printListOfPoints(A):
    return str([ (a.x,a.y) for a in A ])

def printPoint(pt):
    return str(f'{pt.x},{pt.y}')

def tupleToPoint(t):
    x,y = int(t[0]) , int(t[1])
    return Point(x,y)

def pointToTuple(pt):
    return (pt.x , pt.y)

def q(debug_type , debugImg, threshold):
    hsv_filter_vals = HsvFilter(114,0,0,179,255,255,0,0,62,233)
    if(debug_type==1):
        ''' When we're not looking for processed images
        '''
        while(True):
            if(cv.waitKey(1)==ord('q')):
                cv.destroyAllWindows()
                break
            screenshot = wincap.get_screenshot()
            rectangles = debugImg.find(screenshot , threshold)
            output_img = debugImg.drawRectangles(screenshot , rectangles)
            cv.imshow('Matches', output_img)
    if(debug_type==2):
        ''' When we want to test for processed images
        '''
        debugImg.init_control_gui()
        while(True):
            if(cv.waitKey(1)==ord('q')):
                cv.destroyAllWindows()
                break
            screenshot = wincap.get_screenshot()
            processed_img = debugImg.apply_hsv_filter(screenshot)
            cv.imshow('Bot vision' , processed_img)
    if(debug_type==3):
        ''' When we want to see what the bot sees
        '''
        while(True):
            if(cv.waitKey(1)==ord('q')):
                cv.destroyAllWindows()
                break
            screenshot = wincap.get_screenshot()
            processed_img = debugImg.apply_hsv_filter(screenshot, hsv_filter_vals)
            cv.imshow('Bot vision' , processed_img)
    if(debug_type==4):
        ''' When we want to detect needles in processed img haystack (rectangles)
        '''
        while(True):
            if(cv.waitKey(1)==ord('q')):
                cv.destroyAllWindows()
                break
            screenshot = wincap.get_screenshot()
            processed_img = debugImg.apply_hsv_filter(screenshot, hsv_filter_vals)
            rectangles_points = debugImg.find(processed_img , threshold)
            output_img_regu = debugImg.drawRectangles(screenshot , rectangles_points)
            cv.imshow('Matches' , output_img_regu)
    if(debug_type==5):
        ''' When we want to detect needles in processed img haystack (crosshairs)
        '''
        while(True):
            if(cv.waitKey(1)==ord('q')):
                cv.destroyAllWindows()
                break
            screenshot = wincap.get_screenshot()
            processed_img = debugImg.apply_hsv_filter(screenshot, hsv_filter_vals)
            rectangles_points = debugImg.find(processed_img , threshold)
            crosshair_points = debugImg.getClickPoints(rectangles_points)
            output_img_proc = debugImg.drawCrosshairs(processed_img , crosshair_points)
            cv.imshow('Matches' , output_img_proc)

# Use after every click to make sure the points are all valid click points
def qq(array, lock):
    with lock:
        for i in range(10):
            A[i] = Point(0,0)
        printListOfPoints(A)

def qqq(array, lock):
    # No need for lock since we're simply accessing an element while the array is populated
    while(len(array)):
        element = array[0]
        print(f'Clicking on {printPoint(element)}')

# Manipulates the shared array
def qqqq(needleImg , array , runtime, hsv_vals, threshold, lock):
    startTime = time.time()
    while(cv.waitKey(1)!=ord('q') and (time.time() - startTime) < runtime):
        with lock:
            screenshot = wincap.get_screenshot()
            processed_img = needleImg.apply_hsv_filter(screenshot, hsv_vals)
            rectangles_points = needleImg.find(processed_img , threshold)
            crosshair_points = needleImg.getClickPoints(rectangles_points)
            cpoints = [wincap.get_screen_position(c) for c in crosshair_points]
            output_img_proc = needleImg.drawCrosshairs(processed_img , crosshair_points)
            cv.imshow('Matches' , output_img_proc)
            for idx , c in enumerate(cpoints):
                array[idx] = Point(c[0] , c[1])
    cv.destroyAllWindows()

# Uses points in the shared array, doesn't manipulate the array so no lock needed (performance increase)
def qqqqq(array):
    while(len(array)):
        element = array[0]
        pt = pointToTuple(element)
        if(pt != (0,0)):
            speed = randint(15,18)
            deviation = randint(10,60)
            sleepTime = uniform(0.3,0.6)
            moveMouseTo(pt, deviation=deviation, speed=speed, additional_x=10, additional_y=9, sleepTime=0.06)
            click()
            time.sleep(sleepTime)
            with lock:
                resetShared(array,lock) # Remove points we've already clicked on / points that might have disappeared but still appear in array
        else:
            print('No object detected')
            time.sleep(1)

def qqqqqq(array, clickOrder):    
    inputPoint = pointToTuple(array[0])

    # All 3 lists will always have length=28
    inventCoords = []                           # The (x,y) distance from the top inventory bar
    clickPositions = []                         # The actual coordintes which the mouse will click on, calculated based off each inventCoords[i]
    inventPositions = [i for i in range(28)]    # (0,27), each integer represents a position in the inventory
    
    x_vals = [-66,-24,18,60]
    y_vals = [42,79,116,153,190,227,264]
    for x in x_vals:
        for y in y_vals:
            inventCoords.append( (x,y) )        # Generate the list of relative position of each inventory item
    for i in inventCoords:
        clickPositions.append( (i[0]+inputPoint[0] , i[1]+inputPoint[1]) )  # Generate the actual screen position of each inventory item
    positionsDict = dict(zip(inventPositions , clickPositions))     # Each inventory position (0,27) has an absolute click Point (x,y) on the screen

    # clickOrder should be passed as a list of order of items to click on, ex: [1,2,1,3,1,4,1,5 ...]
    for co in clickOrder:
        speed = randint(15,18)
        deviation = randint(10,50)
        pointToClick = positionsDict.get(co)
        moveMouseTo(pointToClick, deviation=deviation, speed=speed, additional_x=12, additional_y=12)
        carefulClick()

def qqqqqqq(images, times, hsvVals, thresholds, inventFlags, nrIterations):
    for ite in range(nrIterations):
        print(f'Iteration : {ite}')
        if(len(images)==len(times)==len(hsvVals)==len(thresholds)):
            for i in range(len(images)):
                if inventFlags[i]==False:   # If we're not interacting with the inventory
                    VisionProcess = Process(target=displayCrosshairs, 
                                            args=(images[i], A, times[i], hsvVals[i], thresholds[i], lock))
                    MovementProcess = Process(target=clickPoint, args=(A, ))
                    VisionProcess.start() 
                    MovementProcess.start()
                    VisionProcess.join(), MovementProcess.terminate()
                    resetShared(A, lock)
                else:
                    '''ORDER'''
                    order = [27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 24, 27, 26, 27, 26, 27, 26, 27, 26, 27, 26, 27, 26, 27, 26, 27, 26, 27, 26, 27, 27, 6, 27, 13, 27, 20]
                    VisionProcess = Process(target=displayCrosshairs, 
                                            args=(images[i], A, times[i], hsvVals[i], thresholds[i], lock))
                    MovementProcess = Process(target=inventClicker, args=(A, order))
                    VisionProcess.start(), MovementProcess.start()
                    VisionProcess.join(), MovementProcess.terminate()

                    resetShared(A, lock)




if __name__ == '__main__':
    print('Done.')
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    