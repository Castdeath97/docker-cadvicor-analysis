import argparse
import numpy
import requests
import time

parser = argparse.ArgumentParser("distr")
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("time", help="Intreval time for requests (seconds)", type=float)
parser.add_argument("param", help="Normal sigma /", type=float)
args = parser.parse_args()

while True : 
    t = abs(numpy.random.normal(args.time, args.sigma, 1)[0])
    time.sleep(t)
    r = requests.get(args.url)
    print("request made after: " + str(round(t,4)) + " server says: \"" + r.text + "\"")