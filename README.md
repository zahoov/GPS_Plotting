# GPS_Plotting

Setting up the GPS Plotting Code (For linux):

Update and Upgrade the computer
sudo apt update
sudo apt upgrade


Download the “GPS_Plotting” repository
git clone https://github.com/zahoov/GPS_Plotting.git


Download the open-elevation repository
git clone https://Zahoov@bitbucket.org/CliveIndrawan/open-elevation-custom-api.git


**Move the Data and Docs folders from the open-elevation repository to the GPS_Plotting repository**


mv open-elevation-custom-api/Data GPS_Plotting

mv open-elevation-custom-api/Docs GPS_Plotting


Install the requisite packages listed:
===================================================================================================
**Basic software that is probably already installed but is required so make sure they are**

sudo apt install python3-pip

sudo apt install curl

sudo apt -y install r-base

GDAL can’t be installed with pip, do the following instead:
===================================================================================================

sudo apt install libgdal-dev gdal-bin

export CPLUS_INCLUDE_PATH=/usr/include/gdal

export C_INCLUDE_PATH=/usr/include/gdal


Python library installation
===================================================================================================

pip install lazy bottle gunicorn rtree pandas pillow


Install extra dependencies
===================================================================================================

sudo apt install pandoc
sudo apt install libudunits2-dev
sudo apt install libfontconfig1-dev

Install R packages, enter R with sudo R, once in R enter:
===================================================================================================

install.packages(“mapview”)

install.packages(“lubridate”)

install.packages(“leaflet”)

install.packages(“tinytex”)

install.packages(“rmarkdown”)

The default PhantomJS install often causes problems with this code so we need to uninstall it and then install the newest version:
===================================================================================================

sudo apt-get install build-essential chrpath libssl-dev libxft-dev

sudo apt-get install libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev 

wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2

sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/ 

sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin 


The plotter can use either raw GPS logs (the direct output of the GPS chip over UART) OR it can use formatted GPS logs in Calvin’s format.
===================================================================================================

For raw GPS logs: Insert these files (multiple is fine as long as they are named appropriately) into the “rawGPS_input” folder

For formatted GPS logs: Insert the file in the “GPSFolder” folder and comment out the:

“sed ‘/^$/d’ rawGPS_input/gps_*.txt | python3 shellTestExtractGPS2.0.py” from Main.sh

Plotting the Data:
===================================================================================================

Run: “python3 server.py”

In a new terminal window run: “sh Main.sh”


The map should be created in the working directory (/GPS_Plotting) in 3 formats: .html, .png, .pdf


