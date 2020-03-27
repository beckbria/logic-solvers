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

"""If you have to increase this number, you must add more entries to AddIntEqualComparisonConstraint"""
MAX_INT_CONSTRAINT = 50

def AddIntEqualComparisonConstraint(solver, z3int, target):
    """
    This performs int comparisons against a finite range of immutable values since Z3
    only operates on immutables.  It's not beautiful code, but it works for basic
    counters.

    To regenerate:
    for i in range(51):
        print('    elif target == {}:'.format(i))
        print('        solver.add(z3int == {})'.format(i))
    """
    if target == 0:
        solver.add(z3int == 0)
    elif target == 1:
        solver.add(z3int == 1)
    elif target == 2:
        solver.add(z3int == 2)
    elif target == 3:
        solver.add(z3int == 3)
    elif target == 4:
        solver.add(z3int == 4)
    elif target == 5:
        solver.add(z3int == 5)
    elif target == 6:
        solver.add(z3int == 6)
    elif target == 7:
        solver.add(z3int == 7)
    elif target == 8:
        solver.add(z3int == 8)
    elif target == 9:
        solver.add(z3int == 9)
    elif target == 10:
        solver.add(z3int == 10)
    elif target == 11:
        solver.add(z3int == 11)
    elif target == 12:
        solver.add(z3int == 12)
    elif target == 13:
        solver.add(z3int == 13)
    elif target == 14:
        solver.add(z3int == 14)
    elif target == 15:
        solver.add(z3int == 15)
    elif target == 16:
        solver.add(z3int == 16)
    elif target == 17:
        solver.add(z3int == 17)
    elif target == 18:
        solver.add(z3int == 18)
    elif target == 19:
        solver.add(z3int == 19)
    elif target == 20:
        solver.add(z3int == 20)
    elif target == 21:
        solver.add(z3int == 21)
    elif target == 22:
        solver.add(z3int == 22)
    elif target == 23:
        solver.add(z3int == 23)
    elif target == 24:
        solver.add(z3int == 24)
    elif target == 25:
        solver.add(z3int == 25)
    elif target == 26:
        solver.add(z3int == 26)
    elif target == 27:
        solver.add(z3int == 27)
    elif target == 28:
        solver.add(z3int == 28)
    elif target == 29:
        solver.add(z3int == 29)
    elif target == 30:
        solver.add(z3int == 30)
    elif target == 31:
        solver.add(z3int == 31)
    elif target == 32:
        solver.add(z3int == 32)
    elif target == 33:
        solver.add(z3int == 33)
    elif target == 34:
        solver.add(z3int == 34)
    elif target == 35:
        solver.add(z3int == 35)
    elif target == 36:
        solver.add(z3int == 36)
    elif target == 37:
        solver.add(z3int == 37)
    elif target == 38:
        solver.add(z3int == 38)
    elif target == 39:
        solver.add(z3int == 39)
    elif target == 40:
        solver.add(z3int == 40)
    elif target == 41:
        solver.add(z3int == 41)
    elif target == 42:
        solver.add(z3int == 42)
    elif target == 43:
        solver.add(z3int == 43)
    elif target == 44:
        solver.add(z3int == 44)
    elif target == 45:
        solver.add(z3int == 45)
    elif target == 46:
        solver.add(z3int == 46)
    elif target == 47:
        solver.add(z3int == 47)
    elif target == 48:
        solver.add(z3int == 48)
    elif target == 49:
        solver.add(z3int == 49)
    elif target == 50:
        solver.add(z3int == 50)
    else:
        raise ValueError('AddIntEqualComparisonConstraint value beyond MAX_INT_CONSTRAINT')