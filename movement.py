import numpy as np
import pyautogui as p
import time
import sourcerandom
import pandas as pd
from random import randint, choice, uniform
from math import ceil

p.MINIMUM_DURATION = 0  # Default: 0.1
p.MINIMUM_SLEEP = 0  # Default: 0.05
p.PAUSE = 0  # Default: 0.1
trng_RAND_GEN = sourcerandom.SourceRandom(source=sourcerandom.OnlineRandomnessSource.QRNG_ANU)

def __pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result)) 
    return result
    
def __make_bezier(xys):

    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = __pascal_row(n - 1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                list(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def __mouse_bez(init_pos, fin_pos, deviation, speed):
    '''
    GENERATE BEZIER CURVE POINTS
    Takes init_pos and fin_pos as a 2-tuple representing xy coordinates
        variation is a 2-tuple representing the
        max distance from fin_pos of control point for x and y respectively
        speed is an int multiplier for speed. The lower, the faster. 1 is fastests
    '''

    #time parameter
    ts = [t/(speed * 100.0) for t in range(speed * 101)]
    
    #bezier centre control points between (deviation / 2) and (deviaion) of travel distance, plus or minus at random
    control_1 = (init_pos[0] + choice((-1, 1)) * abs(ceil(fin_pos[0]) - ceil(init_pos[0])) * 0.01 * uniform(deviation / 2, deviation),
                init_pos[1] + choice((-1, 1)) * abs(ceil(fin_pos[1]) - ceil(init_pos[1])) * 0.01 * uniform(deviation / 2, deviation)
                    )
    control_2 = (init_pos[0] + choice((-1, 1)) * abs(ceil(fin_pos[0]) - ceil(init_pos[0])) * 0.01 * uniform(deviation / 2, deviation),
                init_pos[1] + choice((-1, 1)) * abs(ceil(fin_pos[1]) - ceil(init_pos[1])) * 0.01 * uniform(deviation / 2, deviation)
                    )
        
    xys = [init_pos, control_1, control_2, fin_pos]
    bezier = __make_bezier(xys)
    points = bezier(ts)

    return points

# Moves mouse to a specific point, given a certain speed and deviation,
#   as well as an additional boundary in which the mouse can move to.
# The speed and deviation arguments should be randomly generated before passing to this method.
# The point which the mouse should go to should be the top left of the area you want to click,
#   the additional_x and additional_y should be the bottom right of the area to click
''' __move() behaviour
        --> decreasing speed simply decreases the number of points in the bezier curve,
            therefor theoretically decreasing the time it takes to get from a to b since 
            the mouse has to travel to less points, but the movement is more jolty
        --> the deviation simply increases the arc of the curve, but does not have an effect on the number 
            of points in the curve.

        WARNING : the standard __move() method can be up to 50 pixels off at times when moving cursor over long distances.
        --> if you want ACCURATE mouse movement, call moveMouseTo() twice in succession

        perfect mouse movement : relatively high deviation , relatively high speed to match the deviation.
                                    but if both values are too high, slows down performance
'''

def __move(point, deviation=15, speed=20):
    x1,y1 = p.position()
    startPoint = [x1 , y1]
    endPoint = [point[0] , point[1]]
    path = __mouse_bez(startPoint , endPoint , deviation , speed)
    for pa in path:
        p.moveTo(pa)

def countdown():
    for i in range(0,5):
        print('starting in '+str(5-i))
        time.sleep(1)

def moveMouseTo(point, deviation=15, speed=20, additional_x=0, additional_y=0, sleepTime=0):
    rand_x = trng_RAND_GEN.randint(-additional_x , additional_x)
    rand_y = trng_RAND_GEN.randint(-additional_y , additional_y)
    __point = [point[0]+rand_x , point[1]+rand_y]
    __move(__point, deviation, speed)
    __move(__point, deviation=1, speed=1)
    time.sleep(sleepTime)

def moveMouseAroundSmall():
    pts = trng_RAND_GEN.randint(2,5)
    for _ in range(pts):
        rx,ry = randint(-30,30) , randint(-29,31)
        x,y = p.position()
        pt = (x+rx , y+ry)
        moveMouseTo(pt, deviation=50, speed=80)

def __click():
    t = uniform(0.067,0.091)
    p.mouseDown()
    time.sleep(t)
    p.mouseUp()

def carefulClick():
    __click()

def click():
    clickType = trng_RAND_GEN.randint(1,4)
    for _ in range(clickType):
        __click()

def spamClick():
    nrClicks = trng_RAND_GEN.randint(5,8)
    for _ in range(nrClicks):
        t = uniform(0.095, 0.109)
        p.mouseDown()
        time.sleep(t)
        p.mouseUp()

