from urllib import request


for i in range(1000):
    request.urlopen(f'http://localhost:8000/checkout')
