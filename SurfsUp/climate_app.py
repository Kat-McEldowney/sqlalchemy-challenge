# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#display all avaialbe routes 
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"<h1>Welcome to my Climate API app!</h1>"
        f"<h2>CLick below for cliame data collection information</h2>"
        f"<p><a href='/api/v1.0/precipitation'>Precipitation Data</a></p>"
        f"<p><a href='/api/v1.0/stations'>Station List</a></p>"
        f"<p><a href='/api/v1.0/tobs'>Temperature Observations at most Active Station</a></p>"
    )

#create display for last 12 months of precipitaion
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Starting from the most recent data point in the database. 
    date_end = dt.datetime(2017, 8, 23)
    # Calculate the date one year from the last date in data set.
    date_start = date_end - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between(date_start, date_end)).all()

    # Save the query results as a dictonary
    precip_date_measure = []

    for date, pricp in results:
        precip_dict = {}
        precip_dict[date] = pricp
        precip_date_measure.append(precip_dict)
        
    #return search results/dictonary as a json
    return jsonify(precip_date_measure)

#create page wiht a list of station names
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query for station names
    stations = session.query(Station.station, Station.name,
                             Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Iterate through query results, convert to a dictionary.
    station_list = []
    for id, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["station"] = id
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_list.append(station_dict)

    # Return the JSON representation of dictionary.
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine) 

    #calculate the last 12 months of supplied data
    # Starting from the most recent data point in the database. 
    date_end = dt.datetime(2017, 8, 23)
    # Calculate the date one year from the last date in data set.
    date_start = date_end - timedelta(days=365)

    #query last 12 months of data for the most active station
    twelve_months = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date.between(date_start, date_end)).all()

    # Iterate through query results, convert to a dictionary.
    temp_list= []
    for date, temp in twelve_months:
        temp_dict= {}
        temp_dict[date] = temp
        temp_list.append(temp_dict)
       
    # Return the JSON representation of dictionary.
    return jsonify(temp_list)

  
if __name__ == '__main__':
    app.run(debug=True)
