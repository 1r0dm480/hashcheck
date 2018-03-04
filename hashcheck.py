import requests
import json
import argparse

# Setup argument parser
parser = argparse.ArgumentParser(description="Uses the Hahses.org API to check for a plaintext version of any given hashes.")
parser.add_argument('-s', type=str, action="store", dest="hash", help="Single hash to check (E.g. -s 098f6bcd4621d373cade4e832627b4f6)")
parser.add_argument('-f', type=str, action="store", dest="file", help="File containing line seperated list of hashes to check (E.g. -f hashes.txt)")
parser.add_argument('-c', type=str, action="store", dest="commasep", help="String containing several comma seperated hashes (E.g. -c 098f6bcd4621d373cade4e832627b4f6,fb469d7ef430b0baf0cab6c436e70375)")
parser.add_argument('-k', type=str, action="store", dest="key", help="Your Hashes.org API key", required=True)
args = parser.parse_args()
inputhash = args.hash
inputfile = args.file
inputcsep = args.commasep
API_KEY = args.key

# Create Session
s = requests.Session()
s.headers.update({"User-Agent":"HashCheck"})

def checkMultiple(s, hashes, intype, key):
    # Check multiple hashes
    if intype == "file":
        # Load the hashes and format them
        tmp = open(hashes, "r").read().splitlines()
        hashes = ""
        for t in tmp:
            hashes += t+","
        hashes = hashes[:-1]
    if hashes.count(",") <= 100:
        # Check them against Hashes.org
        check = s.get("https://hashes.org/api.php?key={}&query={}".format(key, hashes)).text
        jsonresult = json.loads(check)
        print("-- Results --")
        for j in jsonresult["result"]:
            if jsonresult["result"][j] == None:
                print("{} - Not Found".format(j))
            else:
                print("{}:{}".format(j, jsonresult["result"][j]["plain"]))
    else:
        print("Error: You can only check a maximum of 100 hashes at a time")

def checkSingle(s, hash, key):
    # Check a single hash against Hashes.org
    check = s.get("https://hashes.org/api.php?key={}&query={}".format(key, hash)).text
    jsonresult = json.loads(check)
    if jsonresult["result"][hash] == None:
        print("-- Results --\nInput Hash: {}\nPlaintext: NOT FOUND\nAlgorithm: UNKNOWN".format(hash))
    else:
        print("-- Results --\nInput Hash: {}\nPlaintext: {}\nAlgorithm: {}".format(hash, jsonresult["result"][hash]["plain"], jsonresult["result"][hash]["algorithm"]))

# Begin
try:
    if API_KEY != None:
        if inputhash != None:
            checkSingle(s, inputhash, API_KEY)

        if inputcsep != None:
            checkMultiple(s, inputcsep, "comma", API_KEY)

        if inputfile != None:
            checkMultiple(s, inputfile, "file", API_KEY)
    else:
        print("Error: You must supply a Hashes.org API key")
except Exception as e:
    print("Error: {}".format(e))
