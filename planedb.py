#!/usr/bin/env python3
#
# Copyright (c) 2019 Johan Kanflo (github.com/kanflo)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import requests as req
import json
import ast

hostname = None
port = 31541

def init(_hostname, _port = 31541):
    global hostname
    global port
    hostname = _hostname
    port = _port

def lookup_aircraft(icao24):
    try:
        resp = req.get("http://%s:%d/aircraft/%s" % (hostname, port, icao24))
        if resp.status_code == 200:
            return ast.literal_eval(resp.text) # Works for single quotes
    except req.exceptions.ConnectionError:
        pass
    return False

def update_aircraft(icao24, data):
    global hostname
    url = "http://%s:%d/aircraft/%s" % (hostname, port, icao24)
    try:
        resp = req.post(url, data = data)
        if resp.status_code == 200:
            return resp.text == "OK"
    except req.exceptions.ConnectionError:
        pass
    return False

def lookup_airport(icao24):
    try:
        resp = req.get("http://%s:%d/airport/%s" % (hostname, port, icao24))
        if resp.status_code == 200:
            return ast.literal_eval(resp.text) # Works for single quotes
    except req.exceptions.ConnectionError:
        pass
    return False

def update_airport(icao24, data):
    global hostname
    url = "http://%s:%d/airport/%s" % (hostname, port, icao24)
    try:
        resp = req.post(url, data = data)
        if resp.status_code == 200:
            return resp.text == "OK"
    except req.exceptions.ConnectionError:
        pass
    return False

def lookup_airline(icao24):
    try:
        resp = req.get("http://%s:%d/airline/%s" % (hostname, port, icao24))
        print(resp.text)
        if resp.status_code == 200:
            return ast.literal_eval(resp.text) # Works for single quotes
    except req.exceptions.ConnectionError:
        pass
    return False

def update_airline(icao24, data):
    global hostname
    url = "http://%s:%d/airline/%s" % (hostname, port, icao24)
    try:
        resp = req.post(url, data = data)
        if resp.status_code == 200:
            return resp.text == "OK"
    except req.exceptions.ConnectionError:
        pass
    return False

def lookup_route(callsign):
    try:
        resp = req.get("http://%s:%d/route/%s" % (hostname, port, callsign))
        if resp.status_code == 200:
            return ast.literal_eval(resp.text) # Works for single quotes
    except req.exceptions.ConnectionError:
        pass
    return False

def update_route(callsign, data):
    global hostname
    url = "http://%s:%d/route/%s" % (hostname, port, callsign)
    try:
        resp = req.post(url, data = data)
        if resp.status_code == 200:
            return resp.text == "OK"
        else:
            print(url)
            print(resp.status_code, resp.text)
    except req.exceptions.ConnectionError:
        pass
    return False


def dump(o):
    if o:
        for k in o:
            print("%20s : %s" % (k, o[k]))
    else:
        print("Not found")

# Use as a CLU tool
if __name__ == "__main__":
    import sys
    init("localhost")
    if len(sys.argv) < 2:
        print("Usage: %s [-q icao24] [-r callsign] [-o airline] [-a airport] [-i icao24 [ -m <manufacturer> -t <type> -o <operator> -r <registration> -s <data source> -I <image url> ] ]" % sys.argv[0])
    else:
        if sys.argv[1] == '-o':
            dump(lookup_airline(sys.argv[2]))
        elif sys.argv[1] == '-a':
            dump(lookup_airport(sys.argv[2]))
        elif sys.argv[1] == '-r':
            dump(lookup_route(sys.argv[2]))
        elif sys.argv[1] == '-q':
            dump(lookup_aircraft(sys.argv[2]))
        elif sys.argv[1] == '-i':
            icao24 = sys.argv[2]
            man = None
            mdl = None
            reg = None
            op = None
            src = None
            img = None
            for i in range(3, len(sys.argv) - 1):
                print(sys.argv[i])
                if sys.argv[i] == '-m':
                    man = sys.argv[i+1]
                elif sys.argv[i] == '-t':
                    mdl = sys.argv[i+1]
                elif sys.argv[i] == '-o':
                    op = sys.argv[i+1]
                elif sys.argv[i] == '-r':
                    reg = sys.argv[i+1]
                elif sys.argv[i] == '-s':
                    src = sys.argv[i+1]
                elif sys.argv[i] == '-I':
                    img = sys.argv[i+1]
                else:
                    pass
                    #print("Unknown switch %s" % sys.argv[i])

            plane = {'manufacturer' : man, 'model' : mdl, 'operator' : op, 'registration' : reg, 'image' : img, 'source' : src}
            print(plane)
            if (update_aircraft(icao24, plane)):
                print("ok")
            else:
                print("Update failed")


"""
Testing:

curl --request POST 'http://127.0.0.1:31541/info/10' --data 'model=A380&operator=SAS&registration=ABC123&source=stdin'
curl --request GET http://127.0.0.1:31541/info/10
curl --request POST 'http://127.0.0.1:31541/info/10' --data 'model=A381'
curl --request GET http://127.0.0.1:31541/info/10
curl --request DELETE http://127.0.0.1:31541/info/10
curl --request POST 'http://127.0.0.1:31541/info/11' --data 'model=A380&operator=SAS&registration=ABC123'
curl --request GET http://127.0.0.1:31541/image/11
curl --request POST 'http://127.0.0.1:31541/image/11' --data 'image=http://image.com/plane.jpg'
curl --request GET http://127.0.0.1:31541/image/11
curl --request DELETE http://127.0.0.1:31541/image/11
curl --request GET http://127.0.0.1:31541/image/11
"""
