import sys
import logging
from random import choice
from urllib import request
from multiprocessing import Pool


NAMES = [
    'Alex',
    'Bob',
    'David',
    'Frank',
]


def send_hellos(n):
    n = n or 100
    for i in range(n):
        name = choice(NAMES)
        print(f'Sending request #{i} to /{name}\r')
        request.urlopen(
            f'http://localhost:8000/{name}'
        )


if __name__ == '__main__':

    try:
        n = int(sys.argv[1])

    except Exception:
        print('Usage e.g. python send_hellos 5')
        sys.exit(1)

    p = Pool(5)
    p.map(send_hellos, [None] * n)