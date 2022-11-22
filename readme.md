# trein?

dom python script die je met fcgiwrap en nginx kunt draaien op een server om
een ical bestand te genereren die je laat weten wanneer de ns weer eens niet
rijdt, maar dan rechtstreeks in je agenda!

## setup

de API key wordt lekker veilig opgeslagen in een plain-text bestand `key`.

hier is een voorbeeld nginx configuratie (snippet die in een server block kan):

```nginx
location /ical/trein.ics {
  gzip off;
  autoindex on;
  fastcgi_pass unix:/var/run/fcgiwrap.socket;
  include /etc/nginx/fastcgi_params;
  fastcgi_param SCRIPT_FILENAME /var/trein/trein.py;
}
```

