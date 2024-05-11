#!/bin/sh
cd "$(dirname "$(readlink -f "$0")")"
echo "HTTP/1.1 200 OK\n"
exec ./venv/bin/python3 ./autoplanner.py
