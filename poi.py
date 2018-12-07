# Author: Ammar Hasan 150454388 November 2018
# Purpose: Make requests to a URL using poisson process

import argparse
import numpy
import requests
import time

# Setup required arguments
parser = argparse.ArgumentParser("poi")
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("lam", 
help="Lambda for Intreval time of requests (ms)", type=float)
args = parser.parse_args() # get arguments

# program loop
while True : 
    # get time using numpy exponential (poi process) and sleep with it
    sleep_time = abs(numpy.random.exponential(args.lam)) 
    time.sleep(sleep_time/1000)

    # make request after sleep and report
    r = requests.get(args.url) 
    print("request made after: " + str(round(sleep_time,4)) 
    + "ms server says: \"" + r.text + "\"")