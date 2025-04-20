import requests
import sqlite3
import os


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

def get_weather_data(cur):
    location = "Chicago"
    date_range = "2025-01-11/2025-04-20"
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date_range}?key=44SZFD9YD4PU6UJDGPBX273CX&include=days&elements=datetime,temp,conditions,precip,preciptype"
    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path + "/" + "weather_and_crime.db")
    # cur = conn.cursor()
    response = requests.get(weather_url)
    data = response.json()
    tbl = []
    for day in data['days']:
        lst = [day['datetime'], day['temp'], day['conditions'], day['precip']]
        tbl.append(lst)
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (date_time TEXT PRIMARY KEY, temp INTEGER, conditions TEXT, precip INTEGER)")
    for days in tbl:
        cur.execute("INSERT OR IGNORE INTO Weather (date_time, temp, conditions, precip) VALUES (?, ?, ?, ?)", days)
    

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "weather_and_crime.db")
    cur = conn.cursor()
    # get_weather_data()
    get_crime_data(cur)
    conn.commit()
    pass

if __name__ == "__main__":
    main()