sed '/^$/d' rawGPS_input/gps_*.txt | python3 shellTestExtractGPS2.0.py

sh getAltitude.sh

python3 plotter.py
