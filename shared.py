#!/bin/python3
import urllib.request
import re
from uuid import uuid4
from bs4 import BeautifulSoup

def get_public_key():
  data = urllib.request.urlopen("https://www.ns.nl/reisplanner").read()
  soup = BeautifulSoup(data, features="lxml")
  data = "\n".join(str(x) for x in soup.select('script:-soup-contains("mlabProductKey")'))
  return re.search(r'mlabProductKey: "([0-9a-f]{32})"', data).group(1)

def read_file(filename):
  f = open(filename, "r")
  r = str(f.read())
  f.close()
  return r
