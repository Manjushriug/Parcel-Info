# Parcel-Info

Steps to run the flask app locally

1. Install the requirements specified in requirements.txt
2. cd to parcelindentifier project folder
3. Run the command set FLASK_APP=app.py(Windows) export FLASK_APP=app.py(Linux or MAC)
4. Run flask run command to launch the flask server locally, default port 5000
5. On the browser in the address bar run http://127.0.0.1:5000/ to land in main page of the app
6. Select the options listed on the mainpage, click on submit to get the parcel info
7. scroll down to see the location of the parcel, click on the marker ro see the info of the parcel.

Requirement Spec:

Data Transformation:
Transform the XML streams(End points) and output the data in json format

Presentation:
Parse the latitude and longitude coordinates from the XML streams and display the location on Google Maps.
Click on the map marker to display the additional details on the map.
