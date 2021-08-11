from NMEAParser import NMEAParser
import pandas as pd
import time
import sys
import datetime as dt
import os


def makeSeriesList(colNames: list, parser: NMEAParser) -> list:
    seriesValues = []

    if parser.attributeMap["latitudeDirection"] == "S":
        parser.attributeMap["latitude"] = -(parser.attributeMap["latitude"])

    if parser.attributeMap["longitudeDirection"] == "W":
        parser.attributeMap["longitude"] = -(parser.attributeMap["longitude"])

    for colName in colNames:
        seriesValues.append(parser.attributeMap[colName])

    return seriesValues


def createNewGPSFile():
    currentHour = str(time.localtime().tm_hour) if time.localtime(
    ).tm_hour >= 10 else "0" + str(time.localtime().tm_hour)
    currentYear = str(time.localtime().tm_year)
    currentMonth = str(time.localtime().tm_mon) if time.localtime(
    ).tm_mon >= 10 else "0" + str(time.localtime().tm_mon)
    currentDate = str(time.localtime().tm_mday) if time.localtime(
    ).tm_mday >= 10 else "0" + str(time.localtime().tm_mday)

    GPSFile = open("./GPSFolder/hydraFL_%s%s%s%s_GPS.txt" %
                   (currentYear, currentMonth, currentDate, currentHour), "w")
    GPSFile.writelines("\t".join([colName for colName in GPSColNames]) + "\n")

    return GPSFile


start = time.time()

GPSColNames = ["timestamp", "latitude",
               "longitude", "GPSQuality",
               "numSatellites", "horizontalDilution",
               "geoidHeight", "geoidUnits",
               "status", "knotSpeed",
               "trackAngle", "date"]

GPSFile = createNewGPSFile()
GGALine = ""
RMCLine = ""

previousStamp = None
GGA = None
RMC = None

# filters gps data from stdin pipe and assigns them to dataframe
for line in sys.stdin:

    if "$GPGGA" in line:
        GGA = NMEAParser(line)

        if GGA.incomplete or GGA.attributeMap["timestamp"] == previousStamp:
            continue

        seriesValues = makeSeriesList(GPSColNames[:8], GGA)
        GGALine = "\t".join([str(value) for value in seriesValues])

    if "$GPRMC" in line:
        RMC = NMEAParser(line)

        if RMC.incomplete or RMC.attributeMap["timestamp"] == previousStamp:
            if not GGA.incomplete:
                GPSFile.writelines(GGALine + "\n")

            continue

        seriesValues = makeSeriesList(GPSColNames[-4:], RMC)
        RMCLine = "\t".join([str(value) for value in seriesValues]) + "\n"

        try:
            if RMC.attributeMap["timestamp"] != GGA.attributeMap["timestamp"]:
                GPSFile.writelines(GGALine + "\n")
                GGALine = "\t".join(["" for i in range(8)])

        except Exception:
            GGALine = "\t".join(["" for i in range(8)])

        RMCLine = "\t".join([str(value) for value in seriesValues]) + "\n"
        newLine = "\t".join([GGALine, RMCLine])
        GPSFile.writelines(newLine)

        if GGA.incomplete:
            previousStamp = RMC.attributeMap["timestamp"]
        else:
            previousStamp = max([GGA.attributeMap["timestamp"],
                                 RMC.attributeMap["timestamp"]])

    if time.time() - start >= 3600:
        GPSFile.close()

        start = time.time()
        GPSFile = createNewGPSFile()

GPSFile.close()
