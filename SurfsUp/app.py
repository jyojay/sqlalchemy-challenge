# Importing required dependences, Python SQL toolkit and Object Relational Mapper
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Importing Flask
from flask import Flask, jsonify

# Creating engine and reflecting database schema
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False # prevent sorting of json keys in alphabetical order

# Retrieving most recent date to be used in two of the routes
session = Session(engine)
recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
date_clc = dt.datetime.strptime(recent_date[0],'%Y-%m-%d').date()
# Calculating the date one year from the recent date in data set.
year_ago =  date_clc - dt.timedelta(days=365)

# Defining list of functions to be used in two of the dynamic routes
sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]

session.close()

# Defining function to calculate min, max and average temperature
def temp_calc(min_max_avg):
    min_max_avg_temp = []
    for min, max, avg in min_max_avg:
        temp_dict = {}
        temp_dict["TMIN"] = min
        temp_dict["TMAX"] = max
        temp_dict["TAVG"] = avg
        min_max_avg_temp.append(temp_dict)
    return(min_max_avg_temp)
# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def welcome():
    """Listing all available api routes."""
    return (
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/yyyy-mm-dd ----------- start date <br/>"
         f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd ----------- start date /end date "
     )

###########################################################
# precipitation route that returns json with the date as the key and the value as the precipitation for last year in database
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creating  session (link) from Python to the DB
    session = Session(engine)

    # Designing a query to retrieve the last 12 months of precipitation data and plot the results. 
    precp_year = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    session.close()

    # Saving the query results as a Pandas DataFrame, defining index and passing on to creaate a dictionary for jasonifying
    
    df = pd.DataFrame(precp_year, columns=['Date', 'Precipitation'])
    df = df.sort_values('Date').dropna(how ='any') # removing NaN values
    df = df.set_index('Date')
    mf = df.to_dict()
    return jsonify(mf)

############################################################
# stations route that returns jsonified data of all stations in the database
@app.route("/api/v1.0/stations")
def stations():
    # Creating  session (link) from Python to the DB
    session = Session(engine)

    # Performing a query to retrieve all unique stations and coresponding staiton names and details using join
    most_act = (session.query(measurement.station, station.name, station.latitude, station.longitude, station.elevation).\
                filter(measurement.station == station.station).group_by(measurement.station).all())
    session.close()

    # Adding result in list for jsonifying
    most_act_list = []
    for code, name, lat, long, elev in most_act:
        most_act_dict = {}
        most_act_dict["station_code"] = code
        most_act_dict["station_name"] = name
        most_act_dict["latitude"] = lat
        most_act_dict["longitude"] = long
        most_act_dict["elevation"] = elev
        most_act_list.append(most_act_dict)
 
    return jsonify(most_act_list)

#############################################################
# tobs route to return jsonified data for the most active station for the last year of data 
@app.route("/api/v1.0/tobs")
def tobs():
    # Creating  session (link) from Python to the DB
    session = Session(engine)

    # Performing a query to retrieve most active station for the last year of data
    x = func.count(measurement.date)
    most_act = (session.query(measurement.station, x).group_by(measurement.station).order_by(x.desc()).first())

    temp_year = session.query(measurement.tobs, measurement.date).filter(measurement.station == most_act[0]).\
    filter(measurement.date >= year_ago).all()

    session.close()

    ## The below piece of code may be used before above session query if most recent date for particular station has to be used 
    ## instead of most recent date in the table as done in jupyter notebook code:
    # recent_date_act = session.query(measurement.date).filter(measurement.station == most_act[0]).\
    # order_by(measurement.date.desc()).first()
    # date_clc_act = dt.datetime.strptime(recent_date_act[0],'%Y-%m-%d').date()
    # year_ago =  date_clc_act - dt.timedelta(days=365)

    # Saving the query results as a Pandas DataFrame, defining index and passing on to create a dictionary for jasonifying
    tobs_df = pd.DataFrame(temp_year, columns=[most_act[0], 'Date'])
    tobs_df = tobs_df.sort_values('Date')
    tobs_df = tobs_df.set_index('Date')
    most_act_dict2 = tobs_df.to_dict()
    return jsonify(most_act_dict2)

############################################################# 
@app.route("/api/v1.0/<start>")
def start(start):

    # Creating  session (link) from Python to the DB
    session = Session(engine)
    min_max_avg =  session.query(*sel).filter(measurement.date >= start)
    session.close()

    min_max_avg_temp = temp_calc(min_max_avg)
    return jsonify(min_max_avg_temp)
    
#############################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Creating  session (link) from Python to the DB
    session = Session(engine)
    min_max_avg =  session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end)
    session.close()
    
    min_max_avg_temp = temp_calc(min_max_avg)
    return jsonify(min_max_avg_temp)

if __name__ == '__main__':
     app.run(debug=True)
