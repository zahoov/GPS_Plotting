from PIL import Image

input_file_location = 1
output_file_location = 1


workingDir = r'C:/Users/Xavier Biancardi/PycharmProjects/TestZone/code-collections/R/'

image1 = Image.open(workingDir + 'map.png')
image1.load()
im1 = Image.new("RGB", image1.size, (255, 255, 255))
im1.paste(image1, mask=image1.split()[3])
im1.save(workingDir + 'DrivingMap.pdf')

































#import plotly.graph_objects as go
#
##token = open(".eyJ1IjoiemFob292IiwiYSI6ImNrcjJ0ZnNoZTJmYTUydWwzb2xyMGo4NDAifQ.SVDj7vCSRu51K1fHNfyaWQ").read()
#
#lats = []
#longs = []
#alts = []
#
#
#fin = open("C:/Users/Xavier Biancardi/PycharmProjects/TestZone/code-collections/R/test.csv", "r")
#lines = fin.readlines()
#fin.close()
#
#for line in lines:
#    lat = line.split(',')[9]
#    long = line.split(',')[10]
#    alt = line.split(',')[15]
#
#    lats.append(lat)
#    longs.append(long)
#
#fig = go.Figure(go.Scattermapbox(
#    mode="markers+lines",
#    lon=longs,
#    lat=lats,
#    marker = {'size': 20, 'symbol': ["bus"]}))
#
#
#
#fig.update_layout(
#    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
#    mapbox={
#        'center': {'lon': 49, 'lat': -122},
#        'style': "stamen-terrain",
#        'center': {'lon': -125, 'lat': 49},
#        'zoom': 12})
#
#fig.show()
#