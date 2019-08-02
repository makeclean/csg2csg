#!/usr/env/python3

# functions for vector manipulation to avoid brining in a numpy dependency
# only ever meant to be used on single row vectors, of length 3

def subtract(v1,v2):
    vec = [0.]*3
    vec[0] = v1[0]-v2[0]
    vec[1] = v1[1]-v2[1]
    vec[2] = v1[2]-v2[2]
    return vec

def add(v1,v2):
    vec = [0.]*3
    vec[0] = v1[0]+v2[0]
    vec[1] = v1[1]+v2[1]
    vec[2] = v1[2]+v2[2]
    return vec

def cross(v1,v2):
    vec = [0.]*3
    vec[0] = (v1[1]*v2[2]) - (v2[1]*v1[2])
    vec[1] = (v1[0]*v2[2]) - (v2[0]*v1[2])
    vec[2] = (v1[0]*v2[1]) - (v2[0]*v1[1])
    return vec
