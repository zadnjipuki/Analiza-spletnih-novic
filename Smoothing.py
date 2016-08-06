__author__ = 'paula'

import numpy
import pylab

def smoothTriangle(data,degree,dropVals=False):
        """performs moving triangle smoothing with a variable degree."""
        """note that if dropVals is False, output length will be identical
        to input length, but with copies of data at the flanking regions"""
        triangle=numpy.array(list(range(degree))+[degree]+list(range(degree))[::-1])+1
        #print(triangle)
        smoothed=[]
        for i in range(degree,len(data)-degree*2):
                point=data[i:i+len(triangle)]*triangle
                smoothed.append(sum(point)/sum(triangle))
        if dropVals: return smoothed
        #print(smoothed)
        smoothed=[smoothed[0]]*int(degree+degree/2)+smoothed
        while len(smoothed)<len(data):smoothed.append(smoothed[-1])
        return smoothed
