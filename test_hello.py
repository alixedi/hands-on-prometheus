import sys
import logging
from random import choice
from urllib import request
from multiprocessing import Pool


NAMES = ['Alex', 'Bob', 'David', 'Frank']


for i in range(1000):
    name = choice(NAMES)
    request.urlopen(f'http://localhost:8000/{name}')
