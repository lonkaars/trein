# trein?

domme python scripts voor openbaar vervoer in nederland in je agenda

`storingen` is een script die je met fcgiwrap en nginx kunt draaien op een
server om een ical bestand te genereren die je laat weten wanneer de ns weer
eens niet rijdt

`autoplanner` neemt een icalendar bestand in (met bijvoorbeeld een rooster), en
vraagt voor elke dag een reisadvies op om bij de vroegste afspraak op tijd te
zijn

## setup

### storingen

de storingen API heeft helaas een API key nodig, maar gelukkig wordt deze
lekker veilig opgeslagen in een plain-text bestand `storingen.key`.

trajectnamen staan op losse regels in `storingen.cfg`, een voorbeeld hiervan
staat in deze repository.

hier is een voorbeeld nginx configuratie (snippet die in een server block kan):

```nginx
location /ical/trein.ics {
  gzip off;
  autoindex on;
  fastcgi_pass unix:/var/run/fcgiwrap.socket;
  include /etc/nginx/fastcgi_params;
  fastcgi_param SCRIPT_FILENAME /var/trein/storingen.fcgi;
}
```

### autoplanner

WIP
