#BusSchedule.py
#Name:
#Date:
#Assignment:

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    content = driver.find_element(By.XPATH, "/html/body").text
    driver.quit()
    return content


def loadTestPage():
    with open("testPage.txt", 'r') as page:
        contents = page.read()
    return contents


def parse_time_string(t):
    """Fixes missing spaces in AM/PM and parses as datetime"""
    t = t.strip().upper()
    # Add a space before AM/PM if missing
    if "AM" in t and " AM" not in t:
        t = t.replace("AM", " AM")
    if "PM" in t and " PM" not in t:
        t = t.replace("PM", " PM")
    return datetime.datetime.strptime(t.strip(), "%I:%M %p")


def isLater(time1, time2):
    return time1 > time2


def getCentralTime():
    utc_now = datetime.datetime.utcnow()
    # Central Time = UTC-5 during Daylight Savings, UTC-6 in winter
    central_now = utc_now - datetime.timedelta(hours=5)
    return central_now


def main():
    url = "https://myride.ometro.com/Schedule?stopCode=2269&routeNumber=11&directionName=EAST"

    # Choose live or test
    # content = loadURL(url)
    content = loadTestPage()

    lines = content.splitlines()
    times = []
    for line in lines:
        if "AM" in line or "PM" in line:
            try:
                parse_time_string(line)
                times.append(line.strip())
            except:
                continue

    now = getCentralTime()
    bus_times = []
    for t in times:
        dt = parse_time_string(t).replace(
            year=now.year, month=now.month, day=now.day)
        if isLater(dt, now):
            bus_times.append(dt)

    bus_times.sort()

    print(f"Current Time {now.strftime('%I:%M %p')}")
    if len(bus_times) >= 1:
        diff1 = int((bus_times[0] - now).total_seconds() / 60)
        print(f"The next bus will arrive in {diff1} minutes.")
    if len(bus_times) >= 2:
        diff2 = int((bus_times[1] - now).total_seconds() / 60)
        print(f"The following bus will arrive in {diff2} minutes.")


main()
