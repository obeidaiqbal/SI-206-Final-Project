import sqlite3
import os
import datetime

# Average temp and incident_reports per week.

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "weather_and_crime.db")
    cur = conn.cursor()
    cur.execute("SELECT Weather.date_time, Weather.temp, Crime.incident_reports FROM Weather INNER JOIN Crime on Weather.date_time = Crime.date_time")
    rows = cur.fetchall()
    with open('calc.txt', 'w') as f:
        f.write("Average Temp and Average Incident_reports each week\n")
        f.write("---------------------------------------------------\n")
        total_temp = 0
        total_reports = 0
        temp_count = 0
        reports_count = 0
        week_count = 1
        for row in rows:
            date_obj = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
            if date_obj.weekday() == 0:
                f.write(f'Week {week_count}: Avg. Temp = {(total_temp/temp_count):.2f}, Avg. Reports = {(total_reports/reports_count):.2f}\n')
                total_temp = row[1]
                total_reports = row[2]
                temp_count = 1
                reports_count = 1
                week_count += 1
            else:
                total_temp += row[1]
                total_reports += row[2]
                temp_count += 1
                reports_count += 1
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()