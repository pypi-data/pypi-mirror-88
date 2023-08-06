#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:50:42 2020

@author: fabian.gebauer
"""

def say_hello(name=None):
    if name is None:
        return "Hello, World!"
    else: 
        return f"Hello, {name}!"
