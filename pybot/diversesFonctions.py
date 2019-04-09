#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
# a robot that finishes within five units of the goal counts as a solution
from collide import distc;
def isSolution(pos,finish_position):
    if distc(pos,finish_position)<=5:
        return True;
    else:
        return False;
    
