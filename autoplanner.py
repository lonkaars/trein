#!/bin/python3
import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import dateutil.parser
import re
from uuid import uuid4
from icalendar import Calendar, Event
from shared import *
import sys
from datetime import datetime

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

# don't calculate trip for events further than a week in the future
FUTURE_MAX = 7 * DAY
# allow trips to end two minutes late (lazy student mode)
LATE_MAX = 2 * MINUTE

cal = Calendar()
KEY = ""
CFG = {}

def get_events():
  c = Calendar.from_ical(sys.stdin.read())
  return list(c.walk('vevent'))

def read_file(filename):
  f = open(filename, "r")
  r = str(f.read())
  f.close()
  return r

def get_trip(date):
  headers = {
    'Ocp-Apim-Subscription-Key': KEY,
    'X-Request-Id': str(uuid4()),
  }
  param_dict = {
    'searchForArrival': True,
    'dateTime': date.isoformat(),
  }
  param_dict.update(CFG)
  params = urllib.parse.urlencode(param_dict)
  conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
  conn.request("GET", f"/reisinformatie-api/api/v3/trips?{params}", "", headers)
  response = conn.getresponse()
  data = response.read()
  conn.close()
  f = open("./autoplanner-api-response.json", "w+")
  f.write(str(data, "utf-8"))
  f.close()
  return data

def leg2desc(leg):
  desc = ""
  duration = leg['plannedDurationInMinutes']
  desc += f"Totale ritduur is {duration} {'minuut' if duration == 1 else 'minuten'}\n\n"

  desc += "Tussenstops:\n"
  for stop in leg['stops']:
    desc += f" - {stop['name']}\n"
  desc += "\n"
  return desc

def trip2ical(trip, real_date):
  trips = trip['trips']
  trips = [t for t in trips if t['status'] != 'CANCELLED']
  trips = [t for t in trips if dateutil.parser.parse(t['legs'][-1]['destination']['plannedDateTime']).timestamp() < (real_date.timestamp() + LATE_MAX)]
  actual_trip = next(reversed(trips))
  if actual_trip == None: return # no trip possible

  for leg in actual_trip['legs']:
    if leg['travelType'] == 'WALK': continue

    ev = Event()
    ev.add('summary', f"{leg['name']} -> {leg['direction']}")
    ev.add('description', leg2desc(leg))
    ev.add('dtstart', dateutil.parser.parse(leg['origin']['plannedDateTime']))
    ev.add('dtend', dateutil.parser.parse(leg['destination']['plannedDateTime']))
    cal.add_component(ev)

def main():
  cal.add('prodid', 'trein')
  cal.add('version', '2.0')

  global KEY, CFG
  KEY = get_public_key()
  CFG = json.loads(read_file("./autoplanner.json"))

  now = datetime.now().timestamp()

  # this is garbage code, but gets a list containing the date/time for each
  # first event of every day after today
  times = list(map(lambda x: x.decoded('dtstart').timestamp(), get_events())) # get event times (epoch)
  times = [(x // DAY, x % DAY) for x in times] # split into days and seconds
  times = [x for x in times if x[1] == min([y[1] for y in times if y[0] == x[0]])] # only leave smallest seconds in day
  times = [x for x in times if now < (x[0] * DAY + x[1]) < (now + FUTURE_MAX)] # only leave after today and until FUTURE_MAX
  times = [datetime.fromtimestamp(x[0] * DAY + x[1]) for x in times] # convert back to datetime

  for time in times:
    trip = get_trip(time)
    trip2ical(json.loads(trip), time)

  print(str(cal.to_ical(), 'utf-8'))

if __name__ == "__main__":
  main()

