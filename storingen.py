#!/bin/python3
import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import dateutil.parser
from icalendar import Calendar, Event
from shared import *

cal = Calendar()

def get_disruptions():
  key = read_file("./storingen.key").strip()
  headers = { 'Ocp-Apim-Subscription-Key': key }
  params = urllib.parse.urlencode({ 'isActive': 'true' })
  conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
  conn.request("GET", f"/reisinformatie-api/api/v3/disruptions?{params}", "{body}", headers)
  response = conn.getresponse()
  data = response.read()
  conn.close()
  f = open("./storingen-api-response.json", "w+")
  f.write(str(data, "utf-8"))
  f.close()
  return data

def disruption2ical(disruption):
  ev = Event()
  ev['uid'] = disruption['id']
  ev.add('summary', f"{disruption['timespans'][0]['cause']['label']} {disruption['title']}")
  description = disruption['expectedDuration']['description'] + "\n\n"
  for timespan in disruption['timespans']:
    description += timespan['situation']['label'] + "\n\n"
    description += timespan['alternativeTransport']['label'] + "\n\n"
  ev.add('description', description)
  ev.add('dtstart', dateutil.parser.parse(disruption['start']))
  ev.add('dtend', dateutil.parser.parse(disruption['end']))
  cal.add_component(ev)

def main():
  cal.add('prodid', 'trein')
  cal.add('version', '2.0')

  disruptions = json.loads(get_disruptions())
  relevant_stations = read_file("./storingen.cfg").strip().split("\n")

  for disruption in disruptions:
    relevant = False
    if 'publicationSections' not in disruption: continue
    for section in disruption['publicationSections']:
      consequence_stations = list(map(lambda x: x['name'], section['consequence']['section']['stations']))
      for i in range(len(relevant_stations)):
        if relevant_stations[(i + 0) % len(relevant_stations)] in consequence_stations and \
           relevant_stations[(i + 1) % len(relevant_stations)] in consequence_stations:
          relevant = True # only relevant if consequence contains current and next station
    if relevant: disruption2ical(disruption)

  print(str(cal.to_ical(), 'utf-8'))

if __name__ == "__main__":
  main()

