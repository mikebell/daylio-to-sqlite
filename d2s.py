import csv
import sqlite3
import time
import datetime

daylio_sql = "daylio.sqlite"
daylio_csv = "daylio_export.csv"

try:
    file = open(daylio_csv, 'r')
    file.close()
except FileNotFoundError:
    print("Daylio export file not found.")
    exit()

try:
    file = open(daylio_sql, 'r')
    con = sqlite3.connect(daylio_sql)
    cur = con.cursor()
    cur.execute("DELETE FROM daylio")
except FileNotFoundError:
    file = open(daylio_sql, 'w')
    con = sqlite3.connect(daylio_sql)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE daylio (year, date, weekday, time, mood, activities, note, timestamp FLOAT);")
    cur = con.cursor()

csv_file = open(daylio_csv, 'r')
read_csv = csv.reader(csv_file)
next(read_csv, None)

for row in read_csv:
    timestamp_string = row[1] + ' ' + row[0] + ' ' + row[3]
    timestamp = time.mktime(datetime.datetime.strptime(timestamp_string, "%d %B %Y %H:%M").timetuple())
    row.append(timestamp)
    cur.execute("INSERT INTO daylio (year, date, weekday, time, mood, activities, note, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", row)

csv_file.close()
con.commit()
con.close()
