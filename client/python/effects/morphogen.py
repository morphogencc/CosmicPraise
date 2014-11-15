from __future__ import division
from itertools import chain
import color_utils
import time
import random
#from colormath.color_objects import *
#from colormath.color_conversions import convert_color
from math import pi, sqrt, cos, sin, atan2, log
twopi = 2 * pi

__all__ = ["cortex"]


def scaledRGBTupleToHSL(s):
    rgb = sRGBColor(s[0], s[1], s[2], True)
    return convert_color(rgb, HSLColor)
    
def HSLToScaledRGBTuple(hsl):
    return convert_color(hsl, sRGBColor).get_value_tuple()

#some utility functions
def sigmoid(x,center,a):
    #logistic sigmoid
    epsilon = 0.0001;
    
    min_param_a = 0.0 + epsilon;
    max_param_a = 1.0 - epsilon;
    a = max(min_param_a, min(max_param_a, a));
    a = (1/(1-a) - 1);

    min_center = 0.0 + epsilon;
    max_center = 1.0 - epsilon;
    center = max(min_center, min(max_center, center));
        
    A = 1.0 / (1.0 + numpy.exp(0 - ((x-center)*a*2.0)));
    B = 1.0 / (1.0 + numpy.exp(a));
    C = 1.0 / (1.0 + numpy.exp(0 - a));

    s = (A-B)/(C-B);
    return s

def delta(x, center, width):
    p = sigmoid(n,center - width/2,0.98)
    q = sigmoid(n, center + width/2, 0.98)
    return p-q

spiralAngle = pi/3.0;
spiralAngleAlt = 2.0*pi - pi/3.0;

#0.2, 0, 0.3, alt - 0.7
def cortex(tower, state,
    sVert = 0.0,
    sHorizon = 0.0,
    sDiag = 0.0,
    sDiagAlt = 0.0,
    sArms = 0.0,
    sRings = 1.0,
    sSpiral = 0.0,
    sSpiralAlt = 0.0,
    vertPeriod = 0.2,
    horizonPeriod = 0.2,
    diagPeriod = 0.2,
    diagAltPeriod = 0.2,
    armPeriod = 0.2,
    ringPeriod = 0.2,
    spiralPeriod = 0.2,
    spiralAltPeriod = 0.2,
    numVert = 0.2,
    numHorizon = 0.2,
    numDiag = 0.2,
    numDiagAlt = 0.2,
    numArms = 0.2,
    numRings = 0.2,
    numSpiral = 0.2,
    numSpiralAlt = 0.2):


    vertPeriod *= 20
    horizonPeriod *= 20
    diagPeriod *= 20
    diagAltPeriod *= 20
    armPeriod *= 20
    ringPeriod *= 20
    spiralPeriod *= 20
    spiralAltPeriod *= 20

    numVert *= 200
    numHorizon *= 200
    numDiag *= 200
    numArms *= 200
    numRings *= 200
    numSpiral *= 200
    numSpiralAlt *= 200
 

    Time = state.time / 6
    for pixel in chain(tower.middle, tower.roofline, tower.spire):
        
        if False:
            cX = pixel['x'] / 4 + 0.5
            cY = pixel['z'] / 14
        else:
            cX = pixel['theta'] / (2.0*pi)
            cY = pixel['z'] / 14
        
        newX = log(sqrt(cX*cX + cY*cY))
        newY = atan2(cX, cY)
        
        color = 0.0
        
        # Vertical Bands
        color += sVert * cos(numVert*cY + vertPeriod*Time)
        # Horizontal Bands
        color += sHorizon * cos(numHorizon*cX + horizonPeriod*Time)
        # Diagonal Bands
        color += sDiag * (cos(2.0*numDiag*(cX*sin(spiralAngle) + cY*cos(spiralAngle)) + diagPeriod*Time))
        # Perpendicular Diagonal bands
        color += sDiagAlt * (cos(2.0*numDiagAlt*(cX*sin(spiralAngleAlt) + cY*cos(spiralAngleAlt)) + diagAltPeriod*Time))
        # Arms
        color += sArms * cos(numArms*newY + armPeriod*Time)
        # Rings
        color += sRings * cos(numRings*newX + ringPeriod*Time)
        # Spirals
        color += sSpiral * (cos(2.0*numSpiral*(newX*sin(spiralAngle) + newY*cos(spiralAngle)) + spiralPeriod*Time))
        # Alt Spirals
        color += sSpiralAlt * (cos(2.0*numSpiralAlt*(newX*sin(spiralAngleAlt) + newY*cos(spiralAngleAlt)) + spiralAltPeriod*Time))
        #overall brightness/color
        color *= cos(Time/10.0)
        

        tower.set_pixel(pixel, (sin( color + Time / 3.0 ) * 0.75), color)
    
    for pixel in chain(tower.railing, tower.base):
        tower.set_pixel(pixel, (pixel['theta'] / twopi + state.time/60) % 1.0, (state.time % 30) / 60 + 0.5)
