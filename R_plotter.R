# Title     : TODO
# Objective : TODO
# Created by: Xavier Biancardi
# Created on: 2021-07-26

library(mapview)
library(rmarkdown)
library(raster)
library(tinytex)
library(leaflet)
library(mapview)
library(lubridate)
library(htmltools)
library(htmlwidgets)
library(ggplot2)
library(gridExtra)
library(scales)
library(png)

f <- file('stdin', 'r')
plugin <- htmlDependency('Leaflet.PolylineDecorator',
                         '1.6.0',
                         src = paste(getwd()),
                         script = 'leaflet.polylineDecorator.js')



registerPlugin <- function(map, plugin) {
  map$dependencies <- c(map$dependencies, list(plugin))
  map
}

#
m <- leaflet() %>%

  registerPlugin(plugin) %>%
  addTiles()

#
speedLimit <- 95 / 3600 * 25
coordLimit <- speedLimit / ((111.0 + 87.9) / 2)
zoomLv <- 13
radius <- 1.19209*10^-7 * 4^zoomLv
pixelSize <- 3.85937*10^-3 * 2^zoomLv
textSize <- 6.83593*10^-3 * 2^zoomLv
weight <- 2.10352*10^-4 * 2^zoomLv
#
#"/Users/Xavier Biancardi/PycharmProjects/TestZone/code-collections/R/test.csv"
##Converts to dataframe
rawData <- read.csv(f)
testData <- subset(rawData, select= -c(X))
#print(rawData)
#
coordinateData <- data.frame("timestamp" = testData$timestamp,
                             "latitude" = testData$latitude,
                             "longitude" = testData$longitude,
                             "group" = NA)

currentGroup <- 1

for (i in 2:nrow(coordinateData)) {
  coordinateData$group[i] = currentGroup
  
  

  deltaLat = abs(coordinateData$latitude[i+1] - coordinateData$latitude[i])
  deltaLong = abs(coordinateData$longitude[i+1] - coordinateData$longitude[i])
  deltaTotal = deltaLat + deltaLong
  
  if (is.na(deltaTotal)) {
    next
  }

  if (deltaTotal > coordLimit) {
    print('yowza')
    currentGroup <- currentGroup + 1
  }

}

for (i in 1:currentGroup) {
  
  routeData = coordinateData[(coordinateData$group == i), ]
  print(i)
  
  if (i == 1){
    line_color = "black"
  }
  else if (i == 2){
    line_color = "red"
}
  else{
    line_color = "blue"
  }

  m <- m %>%
    addPolylines(data = routeData,
                 lat = ~latitude,
                 lng = ~longitude,
                 color = line_color,
                 weight = weight,
                 opacity = 1) %>%
    onRender(sprintf("function(el,x,data) {
                        var i = 0
                        while (i < data.latitude.length) {
                          var dec = L.polylineDecorator([[data.latitude[i], data.longitude[i]],
                                                        [data.latitude[i+1], data.longitude[i+1]]],
                                                          {patterns: [
                                                            {offset: 0, repeat: 100,
                                                            symbol: L.Symbol.arrowHead(
                                                              {pixelSize:%.1f,
                                                                pathOptions:{
                                                                  stroke:true, color:'#000000',
                                                                  fillColor:'#ffa500', fillOpacity:0.5}})}
                                                          ]}).addTo(this);

                        i = i + 350;
                      }
                    }", pixelSize),
             data = routeData)
}
latDifference = abs(max(testData$latitude) - min(testData$latitude))
longDifference = abs(max(testData$longitude) - min(testData$longitude))
vwidth = (0.390625/0.12242 * 2^zoomLv) * latDifference
vheight = (0.190898/0.4964 * 2^zoomLv) * longDifference
#0.170898
averageLat = mean(coordinateData$latitude)
averageLong = mean(coordinateData$longitude)
#
m <- m %>%
  setView(averageLong, averageLat, zoom=zoomLv)



mapshot(m, file = paste(getwd(), 'map.png', sep='/'), url = paste(getwd(), 'map.html', sep='/'), vwidth=vwidth, vheight=vheight, selfcontained=FALSE)

