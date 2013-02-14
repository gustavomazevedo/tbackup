# -*- coding: utf-8 -*-

from os import path
with open(path.abspath(__file__).replace('py','txt'), 'a+') as f:
    for i in range(0, 1024):
        for j in range(0, 1023):
            f.write(str(j % 10))
        f.write('\n')
