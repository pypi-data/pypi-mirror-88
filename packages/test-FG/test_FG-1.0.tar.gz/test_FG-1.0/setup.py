#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 17:12:22 2020

@author: fabian.gebauer
"""


from setuptools import setup

setup(
   name='test_FG',
   version='1.0',
   description='A simple test',
   author='FG',
   author_email='fabian.gebauer@new-work.se',
   packages=['test_FG'],  #same as name
   #install_requires=['bar', 'greek'], #external packages as dependencies
)