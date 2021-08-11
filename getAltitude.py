import sys
import pandas as pd
import json

GPSDfList = []
GPSLines = sys.argv[1].split("\n")

for line in GPSLines:
    df = pd.read_csv(line, sep="\t")
    GPSDfList.append(df)

GPSData = pd.concat(GPSDfList)

locsDict = {
    "locations": [],
}

for i in range(len(df)):
    locsDict["locations"].append(
        {
            "latitude": df["latitude"][i],
            "longitude": df["longitude"][i],
        }
    )
tmpJSON = json.dumps(locsDict)
sys.stdout.write(tmpJSON)
