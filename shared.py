#!/bin/python3
import urllib.request
import re
import os
from uuid import uuid4
from bs4 import BeautifulSoup

def get_public_key():
  data = urllib.request.urlopen("https://www.ns.nl/reisplanner/").read()
  soup = BeautifulSoup(data, features="lxml")
  data = "\n".join(str(x) for x in soup.select('script:-soup-contains("nsAppProductKey")'))
  return re.search(r'nsAppProductKey: "([0-9a-f]{32})"', data).group(1)

def read_file(filename):
  f = open(filename, "r")
  r = str(f.read())
  f.close()
  return r

def debug_output(name, data):
  if not os.path.exists("./debug"): return
  f = open(f"./{name}-api-response.json", "w+")
  f.write(str(data, "utf-8"))
  f.close()
