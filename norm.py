# Author: Ammar Hasan 150454388 November 2018
# Purpose: Make requests to a URL using normal distribution

import argparse
import numpy
import requests
import time

# Setup required arguments
parser = argparse.ArgumentParser("norm")
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("mean", help="Mean intreval time for requests (seconds)", type=float)
parser.add_argument("sigma", help="Standard Deviation for time (seconds)", type=float)
args = parser.parse_args() # get arguments

# program loop
while True : 
    # get time using numpy normal and sleep with it
    sleepTime = abs(numpy.random.normal(args.mean, args.sigma, 1)[0])
    time.sleep(sleepTime)

    # make request after sleep and report
    res = requests.get(args.url)
    print("request made after: " + str(round(sleepTime,4)) 
    + " server says: \"" + res.text + "\"")