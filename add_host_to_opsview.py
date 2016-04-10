#!/usr/bin/python

import os
import sys
import json
import urllib
import urllib2
import argparse
import ConfigParser

# Script options.
parser = argparse.ArgumentParser()
parser.add_argument("--group-name", help="Group name of server.")
parser.add_argument("--server-name", help="Server name.")
parser.add_argument("--server-ip", help="Server IP.")
parser.add_argument("--ini-file", help="Path for ini file.")
args = parser.parse_args()

# Use ini file instead hardcoded values inside the script.
ini_file = args.ini_file

# Check if ini file exists.
try:
    os.path.isfile(ini_file)
except TypeError:
    print "Please make sure %s exists in the script's directory." % (ini_file)
    sys.exit(1)

config = ConfigParser.ConfigParser()
# To make ConfigParser case sensitive. 
config.optionxform = str
config.read(ini_file)

# Use configuration inside .ini file. 
defaults = dict(config.items('defaults'))
templates = dict(config.items('templates'))

# Main info.
opsview_url = defaults["opsview_url"]
opsview_user = defaults["opsview_user"]
opsview_password = defaults["opsview_password"]

# Opsview API teplates are dicts inside list. 
host_templates = [ {"name": template} for template in templates.values() ]

# Check if there is any missing argument. 
if None in [args.group_name, args.server_name, args.server_ip, args.ini_file]:
    parser.print_help()
    sys.exit(1)
else:
    host_group_name = args.group_name
    host_name = args.server_name
    host_ip = args.server_ip

# Connect to Opsview.
opsview_cookies = urllib2.HTTPCookieProcessor()
opsview_opener = urllib2.build_opener(opsview_cookies)

connect_opsview = opsview_opener.open(
  urllib2.Request(opsview_url + "rest/login",
    urllib.urlencode(dict({'username': opsview_user, 'password': opsview_password}))
  )
)

response_text = connect_opsview.read()
response = eval(response_text)

# Check Opsview response.
if not response:
    print("Cannot evaluate %s" % response_text)
    sys.exit()

if "token" in response:
    print("OPSView authentication succeeded")
    print("Token: %s" % response["token"])
    opsview_token = response["token"]
else:
    print("OPSView authentication FAILED")
    sys.exit(1)

# Fetch server info.
url = opsview_url + "rest/serverinfo"
headers = {
    "Content-Type": "application/json",
    "X-Opsview-Username": opsview_user,
    "X-Opsview-Token": opsview_token,
}
request = urllib2.Request(url, None, headers)
#print opsview_opener.open(request).read()

# New host info in JSON format.
host = json.dumps({
    "name": host_name,
    "ip": host_ip,
    "hostgroup": {"name": host_group_name},
    "hosttemplates": host_templates,
    "check_period": {"name" : "24x7"},
    "check_command": {"name": "ping"},
    "icon": {
        "name": "SYMBOL - Server",
        "path": "/images/logos/server_small.png"
    }
})

# API link and headers.
url = opsview_url + "rest/config/host"
headers = {
    "Content-Type": "application/json",
    "X-Opsview-Username": opsview_user,
    "X-Opsview-Token": opsview_token,
}

# Add host to Opsviwe.
request = urllib2.Request(url, host, headers)
try:
    connect_opsview = opsview_opener.open(request)
except urllib2.URLError, e:
    print("Could not add host. %s: %s" % (e.code, e.read()))
    could_not_add_host = True

# Debugging.
#print connect_opsview.read()

# Reload only if host is added.
if 'could_not_add_host' not in locals() or 'could_not_add_host' not in globals():
    url = opsview_url + "rest/reload"
    request = urllib2.Request(url, host, headers)
    try:
      connect_opsview = opsview_opener.open(request)
    except urllib2.URLError, e:
      print("Could reload Opsview.")
