import json
import sqlite3
import time

import requests

with open("settings.json", "r") as file:
    settings = json.load(file)

logging, timeout = settings["logging"], settings["timeout"]

assert isinstance(logging, bool), "logging in settings.json isn't bool"
assert isinstance(timeout, (float, int)), "logging in settings.json isn't float or int"

conn = sqlite3.connect("readings.db", check_same_thread=False)
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "reading" ("status" INTEGER, "time" REAL, "id" INTEGER)')
conn.commit()

c.execute("SELECT * FROM reading ORDER BY ID DESC")

last_record = c.fetchone()

if last_record is None:
    status, _time, _id = (1, time.time(), 1)
else:
    status, _time, _id = (int(last_record[0]), float(last_record[1]), int(last_record[2]))

while True:
    try:
        requests.get("https://www.google.com", timeout=2.5)
        if logging:
            print("Network is up")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        if logging:
            print("Network is down")
        if status:
            status = 0
            _id += 1
            c.execute("INSERT (0, :t, :i) INTO reading", {"t": time.time(), "i": _id})
            conn.commit()
            if logging:
                print("Record added of outage")
        time.sleep(timeout)
        continue
    if not status:
        status = 1
        _id += 1
        c.execute("INSERT (1, :t, :i) INTO reading", {"t": time.time(), "i": _id})
        conn.commit()
        if logging:
            print("Record added of recover")
    time.sleep(timeout)
