import numpy as np
import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h2>Available Routes:</h2><br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/tobs'>Temperatures</a><br/>"
        f"/api/v1.0/[startdate]/[enddate]><br/>"
        f"/api/v1.0/[startdate]<br/>"
        
        
    )


@app.route("/api/v1.0/precipitation")
def precip_results():
    """Return date and precipitation in Hawaii for 1 year"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= datetime.date(2016, 8, 23)).all()

    # Convert list of tuples into normal list
    precip = list(np.ravel(results))

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def weather_stations():
    """Return information about weather stations in Hawaii"""
    session = Session(engine)
    results = session.query(Station.id, Station.station, Station.name,Station.longitude, Station.latitude, Station.elevation).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs_results():
    """Return date and temperature in Hawaii for 1 year"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= datetime.date(2016, 8, 23)).all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>",defaults={'end':None})
@app.route("/api/v1.0/<start>/<end>")
def date_results(start, end):
    """Return average min and max temp for the supplied date range"""
    session = Session(engine)
    if end == None:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    stats = list(np.ravel(results))

    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)