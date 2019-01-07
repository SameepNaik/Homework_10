# Import
import numpy as numpy
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes::<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Dates and Precipitation"""
    # Query dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()
    precip = []
    for rain in results:
        rain_dict = {}
        rain_dict["Date"] = rain.date
        rain_dict["Precipitation"] = rain.prcp
        precip.append(rain_dict)
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Station IDs and Names"""
    # Query station names
    results = session.query(Station.station, Station.name).all()
    station_name = []
    for name in results:
        name_dict={}
        name_dict["Station ID"] = name.station
        name_dict["Station Name"] = name.name
        station_name.append(name_dict)
    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def tobs():
    """Dates and TOBs"""
    # Query dates and tobs
    # Find 1 year from last date
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the date and tobs
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).\
    order_by(Measurement.date).all()
    date_tobs=[]
    for temp in results:
        temp_dict={}
        temp_dict["Date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        date_tobs.append(temp_dict)
    return jsonify(date_tobs)


#@app.route("/api/v1.0/<start>")
#def start():
#    date = (2016, 8, 1)
#    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
#    filter(Measurement.date >= date).all()
#    print(results)

#@app.route("/api/v1.0/<start>/<end>")
#def start():
#    start_date = (2016, 8, 1)
#    end_date = (2016, 9, 1)
#    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
#    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
#    print(results)











if __name__=='__main__':
    app.run(debug=True)