# import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup

app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all passengers
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=year_ago).all()
    session.close()
    # Convert list of tuples into normal list
    precipitation = {date:prcp for date,prcp in results}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    stations_results = session.query(Stations.station).all()
    session.close()

    return jsonify(stations_results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temp info
    results = session.query(Measurement.tobs).filter(func.strftime(Measurement.date) > year_ago)
    session.close()
    
    # Convert list of tuples into normal list
    temperature = {date:tobs for date,tobs in results}
    return jsonify(temperature)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    start = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/start_end")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temp info
    results = session.query(Measurement.tobs).filter(func.strftime(Measurement.date) > year_ago)
    session.close()
    
    # Convert list of tuples into normal list
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)