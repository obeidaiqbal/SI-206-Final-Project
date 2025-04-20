import requests
import sqlite3
import os
import datetime

def get_start_date(cur):
   cur.execute("SELECT COUNT(*) FROM Weather")
   count = cur.fetchone()[0]
   if count == 0:
       return '2025-01-01'
   else:
       cur.execute("SELECT date_time FROM Weather ORDER BY id DESC LIMIT 1")
       date = cur.fetchone()[0]
       return date

def get_crime_data(cur):
    crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    cur.execute('SELECT date_time FROM Weather')
    dates = cur.fetchall()
    cur.execute("CREATE TABLE IF NOT EXISTS Crime (id INTEGER PRIMARY KEY AUTOINCREMENT, incident_reports INTEGER, date_time TEXT)")
    for date in dates:
        date = date[0]
        params = {
            "$where": f"date between '{date}T00:00:00' and '{date}T23:59:59'",
            "$select": "count(*)"
        }
        response = requests.get(crime_url, params=params)
        if response.status_code == 200:
            data = response.json()
            cur.execute("INSERT OR IGNORE INTO Crime (incident_reports, date_time) VALUES (?,?)", (data[0]['count'], date))  
        else:
            return f"Error: {response.status_code}, Message: {response.text}"

def get_weather_data(cur, start_date, end_date):
    location = "Chicago"
    date_range = f"{start_date}/{end_date}"
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date_range}?key=44SZFD9YD4PU6UJDGPBX273CX&include=days&elements=datetime,temp,conditions,precip,preciptype"
    response = requests.get(weather_url)
    data = response.json()
    tbl = []
    for day in data['days']:
        lst = [day['datetime'], day['temp'], day['conditions'], day['precip']]
        tbl.append(lst)
    for days in tbl:
        cur.execute("INSERT OR IGNORE INTO Weather (date_time, temp, conditions, precip) VALUES (?, ?, ?, ?)", days)
    

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "weather_and_crime.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Weather (id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, temp INTEGER, conditions TEXT, precip INTEGER)")

    date_ans = get_start_date(cur)
    date_1 = datetime.datetime.strptime(date_ans, "%Y-%m-%d").date()
    start_date = date_1 + datetime.timedelta(days=1)
    end_date = date_1 + datetime.timedelta(days=25)
    print(start_date,end_date)

    get_weather_data(cur, start_date, end_date)

    conn.commit()
    conn.close()
    pass

if __name__ == "__main__":
    main()