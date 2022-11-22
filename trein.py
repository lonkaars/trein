#!/bin/python3
import http.client, urllib.request, urllib.parse, urllib.error, base64

def read_file(filename):
  f = open(filename)
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
  return fake_disruptions()

if __name__ == "__main__":
  print(get_disruptions())
