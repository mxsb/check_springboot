#!/usr/bin/env python
import argparse
import requests
import sys
import json

def info():
    print ("A Nagios plugin for checking springboot service using API")


def check_springboot_service():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protocol', type=str, default='http', choices=['http', 'https'] , help='default http')
    parser.add_argument('--host', type=str, default='localhost', help='the host name or IP; default localhost')
    parser.add_argument('--port', type=int, default=8080, help='default 8080')
    parser.add_argument('--endpoint', type=str, default='/health', help='default /health')
    parser.add_argument('--timeout', type=float, default=5.0, help='timeout in seconds; default 5.0')
    parser.add_argument('--user', type=str, required=False, help='user for HTTP basic authentication')
    parser.add_argument('--password', type=str, required=False, help='password for HTTP basic authentication')
    parser.add_argument('--details', type=bool, default=False, required=False, help='collects JSON elements with status other than "UP" on errors')
    args = parser.parse_args()

    try:
        response = requests.get('{0}://{1}:{2}{3}'.format(args.protocol, args.host, args.port, args.endpoint), timeout=args.timeout, auth=(args.user, args.password)).json()
        status = response['status'] 
    except Exception as error:
        print 'ERROR' # can be replaced with UNKNOWN
        print '{0} {1}'.format(type(error), error)
        sys.exit(3)

    if status == 'UP':
        print status # can be replaced with 'OK'
        sys.exit(0)
    else:
        print status
        if args.details:
            print json.dumps(collect_details(response))
        sys.exit(2)

def collect_details(response):
    details = {}
    for key in response:
        value = response[key]
        if type(value) is dict and value['status'] != 'UP':
            details[key] = value

    return details

check_springboot_service()