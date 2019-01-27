import logging
from random import choice
from urllib import request


NAMES = [
    'Alex',
    'Bob',
    'David',
    'Frank',
]


for i in range(10):
    name = choice(NAMES)
    print(f'Sending request #{i} to /{name}\r')
    request.urlopen(
        f'http://localhost:8000/{name}'
    )
