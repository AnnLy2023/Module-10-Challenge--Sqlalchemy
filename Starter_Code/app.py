import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine, text
from flask import Flask, jsonify
import json


#Flask setup 
app= Flask(__name__)
# Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"""<h1>Available Routes:</h1><br/>
        <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>
        <a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>
        <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/>
        <a href="/api/v1.0/2016-08-23">/api/v1.0/02016-08-23</a><br/>
        <a href="/api/v1.0/2016-08-23/2016-09-23">/api/v1.0/2016-08-23/2016-09-23</a><br/>"""
    ) 
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Get Precipitation"""
    query = text("""
                SELECT
                    station,
                    prcp
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23';               
            """)
    df=pd.read_sql(query, engine)
    data=json.loads(df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/stations")
def stations():
    """Get Stations"""
    query = text("""
                SELECT                   
                    station,
                    count(*) as num_obs
                FROM
                    measurement
                group by 
                    station
                order by 
                    num_obs desc;
            """)
    df=pd.read_sql(query, engine)
    data=json.loads(df.to_json(orient="records"))
    return(data)



@app.route("/api/v1.0/tobs")
def temperature():
    query = text("""
                SELECT
                    date,
                    station,
                    tobs as temperature
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23'
                    and station = 'USC00519281'
            """)

    df = pd.read_sql(query, engine)
    data = json.loads(df.to_json(orient="records"))
    return(data)


@app.route("/api/v1.0/<start>")
def temperature_start(start):
    """Get Stations"""
    query = text(f"""
                SELECT
                    station,
                    min(prcp) as tmin,
                    avg(prcp) as tmean,
                    max(prcp) as tmax
                FROM
                    measurement
                where
                    date >= '{start}';
            """)
    
    df = pd.read_sql(query, engine)
    data = json.loads(df.to_json(orient="records"))
    return(data)


@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start,end):
    """Get Stations"""
    query = text(f"""
                SELECT
                    station,
                    min(prcp) as tmin,
                    avg(prcp) as tmean,
                    max(prcp) as tmax
                FROM
                    measurement
                where
                    date >= '{start}'
                    and date <='{end}'; 
            """)
    
    df = pd.read_sql(query, engine)
    data = json.loads(df.to_json(orient="records"))
    return(data)

# run the website
if __name__ == '__main__':
    app.run(debug=True)
