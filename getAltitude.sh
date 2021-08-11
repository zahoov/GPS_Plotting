GPSInput=$(ls ./GPSFolder/*GPS.txt)


python3 getAltitude.py $GPSInput > tmpJSON

curl -X POST \
	http://localhost:8080/api/v1/lookup \
	-H 'Accept: application/json' \
	-H 'Content-Type: application/json' \
	-d @tmpJSON \
	-o tmpJSON

python3 appendAltitude.py $GPSInput | Rscript R_plotter.R
rm tmpJSON
