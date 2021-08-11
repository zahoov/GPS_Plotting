import json
import sys
import pandas as pd
import datetime as dt
import math
import time

GPSDfList = []

GPSLines = sys.argv[1].split("\n")

for line in GPSLines:
    df = pd.read_csv(line, sep="\t")
    GPSDfList.append(df)

GPSData = pd.concat(GPSDfList)
GPSData["altitude"] = None

jsonFile = open("tmpJSON", "r")
data = json.load(jsonFile)


for i in range(len(data["results"])):
    try:
        GPSData["altitude"][i] = data["results"][i]["elevation"]
    except Exception:
        pass

currentHour = str(time.localtime().tm_hour) if time.localtime(
).tm_hour >= 10 else "0" + str(time.localtime().tm_hour)
currentYear = str(time.localtime().tm_year)
currentMonth = str(time.localtime().tm_mon) if time.localtime(
).tm_mon >= 10 else "0" + str(time.localtime().tm_mon)
currentDate = str(time.localtime().tm_mday) if time.localtime(
).tm_mday >= 10 else "0" + str(time.localtime().tm_mday)

GPSData.to_csv("hydraFL_%s%s%s%s_GPS.txt" %
               (currentYear, currentMonth, currentDate, currentHour), sep="\t")
GPSData = GPSData.dropna(how="any")
GPSData = GPSData.reset_index(drop=True)
GPSData.to_csv("cmonwork.csv")

latConversion = 111.0
longConversion = 87.9
cumulativeDistance = 0
firstIndex = 0
#print(GPSData["date"])

#for key, value in GPSData.items():
#    print(key, value)
    
#print(len(GPSData))
headTime = dt.datetime.combine(
    dt.datetime.strptime(GPSData["date"][firstIndex], "%Y-%m-%d"),
    dt.datetime.strptime(GPSData["timestamp"][firstIndex], "%H:%M:%S").time())

for i in range(len(GPSData)):

    tailTime = dt.datetime.combine(
        dt.datetime.strptime(GPSData["date"][i], "%Y-%m-%d"),
        dt.datetime.strptime(GPSData["timestamp"][i], "%H:%M:%S").time())
    diff = tailTime - headTime

    if diff.seconds >= 300:
        for j in range(firstIndex, i):
            x1 = GPSData["latitude"][j]
            x2 = GPSData["latitude"][j+1]
            y1 = GPSData["longitude"][j]
            y2 = GPSData["longitude"][j+1]

            absX = abs(x1 - x2) * latConversion
            absY = abs(y1 - y2) * longConversion

            displacement = math.sqrt(absX**2 + absY**2)
            cumulativeDistance = cumulativeDistance + displacement

        if cumulativeDistance < 0.25:
            GPSData.drop([*range(firstIndex, i+1)])

        firstIndex = i + 1
        cumulativeDistance = 0
        headTime = dt.datetime.combine(
            dt.datetime.strptime(GPSData["date"][firstIndex], "%Y-%m-%d"),
            dt.datetime.strptime(GPSData["timestamp"][firstIndex], "%H:%M:%S").time())


#fout = open("notsurewhatthisis.txt", 'r')
# Creates a dataframe of 1-second increments from 0.25-second increments

dataframe = GPSData

qualityFilter = dataframe["GPSQuality"] != 6
statusFilter = dataframe["status"] != "V"
dataframe = dataframe[qualityFilter]
dataframe = dataframe[statusFilter]
dataframe = dataframe.dropna(how="any")

sys.stdout.write(dataframe.to_csv(sep=","))

