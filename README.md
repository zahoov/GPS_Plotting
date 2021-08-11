# README #

This API is a customized open-source elevation API taken from [https://www.open-elevation.com/](https://www.open-elevation.com/).

The files already contain geographic data from the Lower Mainland up until Whistler.

### Setting up the server ###

* Run server.py in a terminal
* The database can now be accessed via localhost:8080
* To make a request, use curl POST or GET (see [https://www.open-elevation.com/](https://www.open-elevation.com/) for more information)

Example:
```
curl -X POST \
        http://localhost:8080/api/v1/lookup \
        -H 'Accept: application/json' \
        -H 'Content-Type: application/json' \
        -d @tmpJSON \
        -o tmpJSON
```

### Adding data to the database ###

* Obtain the desired geographic data from [http://srtm.csi.cgiar.org/srtmdata/](http://srtm.csi.cgiar.org/srtmdata/)
* Move the data to this folder, and run create-dataset.sh passing the data as argument
* Restart the server. The new data should now be included.

### Required Python libraries ###
* lazy
* GDAL
* bottle
* gunicorn
* rtree

See requirements.txt for specific information on the version.
