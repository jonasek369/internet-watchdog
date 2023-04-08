import sqlite3
import time

conn = sqlite3.connect("readings.db", check_same_thread=False)
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "reading" ("status" INTEGER, "time" REAL, "id" INTEGER)')


c.execute("SELECT * FROM reading ORDER BY ID ASC")

records = c.fetchall()

last_record = []
for status, _time, _id in records:
    status = int(status)
    if status:
        last_record = [status, _time, _id]
        continue
    etime = time.gmtime(last_record[1])
    print(f"{etime.tm_mday}-{etime.tm_mon}-{etime.tm_year} {etime.tm_hour}:{etime.tm_min}:{etime.tm_sec} outage took {_time - last_record[1]} seconds")