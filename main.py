import requests

location = "Chicago"
date_range = "2025-04-01/2025-04-01"
weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date_range}?key=9QWKR8DW943NL88PUGYQDLC3C"
crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"


def get_crime_data():
    date = "2024-04-04"
    params = {
        "$where": f"date between '{date}T00:00:00' and '{date}T23:59:59'",
        "$select": "count(*)"
    }
    response = requests.get(crime_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["count"]
        else:
            return f"No data found for {date}."
    else:
        return f"Error: {response.status_code}, Message: {response.text}"

def get_weather_data():
    response = requests.get(weather_url)
    data = response.json()
    tbl = []
    for day in data['days']:
        lst = [day['datetime'], day['conditions']]
        tbl.append(lst)
    return tbl

def main():
    print(f"Weather Conditions: {get_weather_data()}")
    print(f"Incident Reports: {get_crime_data()}")

if __name__ == "__main__":
    main()