#! /usr/bin/env python

# Recursively list all python files under a directory
import os
import sys

if (len(sys.argv) < 2):
    path = '.'
else:
    path = sys.argv[1]

files = [os.path.join(root, file)
         for root, dirs, files in os.walk(path)
         for file in files
         if file.endswith('.py')]
# print("python files under ", path)
print(*files, sep='\n')
