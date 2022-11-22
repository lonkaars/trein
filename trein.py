#!/bin/python3
import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import dateutil.parser
from icalendar import Calendar, Event

cal = Calendar()
cal.add('prodid', 'trein')
cal.add('version', '2.0')

def read_file(filename):
  f = open(filename, "r")
  r = str(f.read())
  f.close()
  return r

def fake_disruptions():
  return read_file("./api_response.json")

def real_disruptions():
  key = read_file("./key").strip()
  headers = { 'Ocp-Apim-Subscription-Key': key }
  params = urllib.parse.urlencode({ 'isActive': 'true' })
  conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
  conn.request("GET", f"/reisinformatie-api/api/v3/disruptions?{params}", "{body}", headers)
  response = conn.getresponse()
  data = response.read()
  conn.close()
  return data

def get_disruptions():
  return real_disruptions()

def disruption2ical(disruption):
  ev = Event()
  ev['uid'] = disruption['id']
  ev.add('name', f"{disruption['timespans'][0]['cause']['label']} {disruption['title']}")
  description = disruption['expectedDuration']['description'] + "\n\n"
  for timespan in disruption['timespans']:
    description += timespan['situation']['label'] + "\n\n"
    description += timespan['alternativeTransport']['label'] + "\n\n"
  ev.add('description', description)
  ev.add('dtstart', dateutil.parser.parse(disruption['start']))
  ev.add('dtend', dateutil.parser.parse(disruption['end']))
  cal.add_component(ev)

def main():
  disruptions = json.loads(get_disruptions())
  relevant_stations = read_file("./config").strip().split("\n")

  for disruption in disruptions:
    relevant = False
    for section in disruption['publicationSections']:
      consequence_stations = list(map(lambda x: x['name'], section['consequence']['section']['stations']))
      for i in range(len(relevant_stations)):
        if relevant_stations[(i + 0) % len(relevant_stations)] in consequence_stations and \
           relevant_stations[(i + 1) % len(relevant_stations)] in consequence_stations:
          relevant = True # only relevant if consequence contains current and next station
    if relevant: disruption2ical(disruption)

  print(cal.to_ical())

if __name__ == "__main__":
  main()

