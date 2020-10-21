from flask import Flask,render_template,request
from bs4 import BeautifulSoup
import requests
import xmltodict
import json
import os
from flask_googlemaps import GoogleMaps, Map, icons

app = Flask(__name__)

GoogleMaps(app)

keylist = []
valuelist = []
dictkeyslist = []
latitude = '37.4300'
longitude = '-122.1400'
parcelid = ''
owner = ''
state = ''
zip = ''
street = ''

#Function to convert XML response to JSON
def printallkeys(json_object):
    global keylist
    global valuelist,street,state,zip
    global dictkeyslist,longitude,latitude,parcelid,owner
    for key,value in json_object.items():
        if type(value) is dict:
            keylist.append((key,None))
            if key == 'LATITUDE':
                latitude = value['value']
                print(latitude)
            
            if key == 'LONGITUDE':
                longitude = value['value']
                print(longitude)

            if key == "towner":
               owner = value['value']

            if key == "MAIL_STREET_SUFFIX":
               street = value['value']

            if key == "MAIL_STATE":
                state = value['value']
            if key == "MAIL_ZIPCODE":
                zip = value['value']
            printallkeys(value)

        else:
            if type(value) is not list:
                if key == 'id':
                    parcelid = value
                
                if value == None:
                    value = 'N/A'
                keylist.append((key,value))
               

        if type(value) is list:
            for i in value:
                keylist.append((key,None))
                printallkeys(i)
    return keylist

#Create Google Map with the specified latitude and longitude
def map_view(latitude,longitude):
    global parcelid
    Idinfo = 'ID:'+ parcelid
    
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=latitude,
        lng=longitude,
        markers=[{
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat':  latitude,
            'lng':  longitude,
            'infobox': "<p>"+Idinfo+"</p>" "<p>"+'Owner:' + owner + "</p>""<p>"+'Street:' + street +"</p>""<p>"+'State:' + state +"</p>""<p>"+'Zip:' + zip +"</p>"
        }],
        style="height:100%;width:100%;margin:0;background-color:black;",
    )

    return  gmap

#Route for Landing page
@app.route("/")
def hello():
    
    gmap = map_view(latitude,longitude)
    return render_template("map.html",gmap=gmap)

#Route for get the parcel info
@app.route("/getParcelInfo", methods=['GET','POST'])
def handle_parcel():
    global keylist,valuelist,dictkeyslist,longitude,latitude
    
    keylist = []
    valuelist = []
    endPoint = "http://neocando.case.edu/cando/housingReport/lbxml.jsp?parcel="
    save_path_file = ".\\result.xml"
    xml_str = ""
    
    parcelId = request.form['options']
    

    endpoint = endPoint + parcelId

    result = requests.get(endpoint)

    for line in result.text:
        if line != "<?xmlversion='1.0'?>":
            line = line.strip()
    
            xml_str += line
        else:
            xml_str += line

    with open(save_path_file, "w") as f: 
        f.write(BeautifulSoup(xml_str, "xml").prettify())

    with open(".\\result.xml") as fd:
        doc = xmltodict.parse(fd.read())
        json_data = json.dumps(doc)

    with open(".\\data.json", "w") as json_file: 
        json_file.write(json_data) 
        json_file.close()
    
    with open('.\\data.json', 'r') as json_file:
        json_object = json.load(json_file)

    list1= printallkeys(json_object)

    imagesource = parcelid + ".jpg"

    #Create Google Map
    gmap = map_view(latitude,longitude)

    return render_template("map.html",heading="Parcel Info",mapheader="Location of the parcel",imagesource=imagesource,keyslist=list1,gmap=gmap)

if __name__ == "__main__":
    app.run(debug=True)