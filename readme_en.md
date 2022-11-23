# trein

janky python scripts for putting dutch public-transit stuff in your calendar
using python, fcgiwrap and nginx

`storingen.py` creates an ical file with current service disriptions affecting
certain route sections

`autoplanner.py` takes an ical schedule as input, and uses the NS API to get
trip advice for the first event of each day in the input schedule

## setup

### service disriptions

`storingen.py` requires an NS API key, which is stored as plain-text in
`storingen.key`.

station names are on seperate lines in `storingen.cfg`. an example file is
included in this repo.

### autoplanner

this one uses the public trip planner on the NS website to request trip advice
from the API. because this is not an officially supported way to use the API,
this script might break in the future.

`autoplanner.py` expects a file `autoplanner.json`, containing to/from location
coordinates, and reads the input ical schedule from stdin. an example format of
`autoplanner.json` file is included in `autoplanner.def.json`.

script call example (edit `autoplanner.fcgi` for server use):

```bash
./autoplanner.py < schedule.ics
# or
curl https://schedule.provider/schedule.ics | ./autoplanner.py
```

### nginx

here's an example nginx config snippet (valid in server block) for calling
these scripts on certain endpoints:

```nginx
location /ical/trein.ics {
  gzip off;
  autoindex on;
  fastcgi_pass unix:/var/run/fcgiwrap.socket;
  include /etc/nginx/fastcgi_params;
  fastcgi_param SCRIPT_FILENAME /var/trein/storingen.fcgi;
}
```
