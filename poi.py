# Author: Ammar Hasan 150454388 November 2018
# Purpose: Make requests to a URL using poisson distribution

import argparse
import numpy
import requests
import time

# Setup required arguments
parser = argparse.ArgumentParser("poi")
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("lam", help="Lambda for Intreval time of requests (seconds)", type=float)
args = parser.parse_args() # get arguments

# program loop
while True : 
    # get time using numpy poission and sleep with it
    t = abs(numpy.random.poisson(args.lam)) 
    time.sleep(t)

    # make request after sleep and report
    r = requests.get(args.url) 
    print("request made after: " + str(round(t,4)) + " server says: \"" + r.text + "\"")