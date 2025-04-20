import matplotlib
import matplotlib.pyplot as plt
import requests
import sqlite3
import os


def make_first_plot(cur):
    cur.execute("SELECT Weather.date_time, Weather.conditions, Crime.incident_reports FROM Weather JOIN Crime ON Weather.date_time = Crime.date_time")
    tbl = cur.fetchall()
    conditions = [row[1] for row in tbl]
    incidents = [int(row[2]) for row in tbl]
    grouped = {}
    for cond, count in zip(conditions, incidents):
        if cond in grouped:
            grouped[cond] += count
        else:
            grouped[cond] = count   
    grouped = sorted(grouped.items(), key=lambda x: x[1])
    conditions = [item[0] for item in grouped]
    incidents = [item[1] for item in grouped]
    plt.bar(conditions, incidents)
    plt.xlabel("Weather Conditions")
    plt.ylabel("Incident Reports")
    plt.title("Crime Reports by Weather Condition")
    plt.xticks(rotation = 45)
    plt.savefig('incidents_by_condition.png')
    plt.close()

def make_second_plot(cur):
    cur.execute("SELECT Weather.date_time, Weather.temp, Crime.incident_reports FROM Weather JOIN Crime ON Weather.date_time = Crime.date_time")
    tbl = cur.fetchall()
    dates = [row[0] for row in tbl]
    temps = [int(row[1]) for row in tbl]
    incidents = [int(row[2]) for row in tbl]
    combined = sorted(zip(temps, incidents), key=lambda x: x[0])
    temps, incidents = zip(*combined)
    plt.scatter(temps, incidents)
    plt.xlabel("Temperature (°F)")
    plt.ylabel("Incident Reports")
    plt.title("Incident Reports by Temperature")
    plt.savefig('incidents_by_temperature.png')
    plt.close()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "weather_and_crime.db")
    cur = conn.cursor()
    make_first_plot(cur)
    make_second_plot(cur)
    conn.close()

if __name__ == "__main__":
    main()