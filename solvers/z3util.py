"""Reusable helper functions for Z3 python wrappers"""
from collections import defaultdict
from z3 import *

def IsOdd(i):
    """Returns a Z3 condition for if an Int is odd"""
    return i % 2 != 0

def IsEven(i):
    """Returns a Z3 condition for if an Int is even"""
    return i % 2 == 0

def NumberFromDigits(*args):
    """Given an array of Int digits, returns an Int as if they were read left-to-right"""
    num = 0
    for arg in args:
        num = (10 * num) + arg
    return num

def Z3IntArray(size, prefix):
    """Creates an array of new Z3 Int objects.  They will be named prefix0-prefix[size-1]"""
    arr = []
    fmt = prefix + '{num:02d}'
    for i in range(size):
        arr.append(Int(fmt.format(num=i)))
    return arr

def Z3IntDict2D(width, height, prefix):
    """
    Returns a dict keyed on (X,Y) tuples of new Z3 Int objects.  They will be named
    prefix-X-Y.  The upper-left corner is (0,0) and the grid proceeds down and right
    from there.

    width: Width of the grid (int)
    height: Height of the grid (int)
    prefix: Unique string prefix to identify the Z3 variables
    """
    d = defaultdict(lambda: None)
    for x in range(width):
        for y in range(height):
            d[(x,y)] = Int(Z3IntDictKey(x,y,prefix))
    return d

def Z3IntDictKey(x, y, prefix):
    """Returns the Z3 variable name for a grid space created by Z3IntDict2D"""
    fmt = prefix + '-{}-{}'
    return fmt.format(x,y)