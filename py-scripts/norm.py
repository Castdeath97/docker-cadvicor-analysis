# Author: Ammar Hasan 150454388 November 2018
# Purpose: Make requests to a URL using normal distribution

import argparse
import numpy
import requests
import time

# Setup required arguments
parser = argparse.ArgumentParser("norm")
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("mean", 
help="Mean intreval time for requests (ms)", type=float)
parser.add_argument("sigma", 
help="Standard Deviation for time (ms)", type=float)
args = parser.parse_args() # get arguments

# program loop
while True : 
    # get time using numpy normal and sleep with it
    sleep_time = abs(numpy.random.normal(args.mean, args.sigma, 1)[0])
    time.sleep(sleep_time/1000)

    # make request after sleep and report
    res = requests.get(args.url)
    print("request made after: " + str(round(sleep_time,4)) 
    + "ms server says: \"" + res.text + "\"")