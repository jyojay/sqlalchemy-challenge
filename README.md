# sqlalchemy-challenge

This repository contains:
* Folder **SurfsUp** consisting of the following:
  *   Folder **Resources** with sqllite db and 2 csv files provided
  *   **climate_starter.ipynb** with jupyter notebook script Analysing and Exploring the Climate Data
  *   **app.py** with python script for climate app

# Notes:
* Jupyter notebook and Python 3.11 used
* **climate_starter.ipynb**
  *   Python and SQLAlchemy are used to do a basic climate analysis and data exploration of climate database. SQLAlchemy ORM queries, Pandas, and Matplotlib have been used for the same.
  *    Exploratory Precipitation Analysis for the last 12 months of precipitation data has been done and Pandas Plotting with Matplotlib used to plot it into a line graph with **date in x axis and precipitation in 'mm' in the y axis**
  *    Summary statistics have been determined for this data using pandas dataframe '**describe**' function
  *    Exploratory Station Analysis for the most active station (i.e. which stations have the most rows?) has been done
  *    Lowest, highest, and average temperature for the most active station **USC00519281** has been calculated using '**func**' functions
  *    Querying the last 12 months of temperature observation data for this station, results are plotted in a histogram using 12 bins
* **app.py**
  *    A landing page with all available routes, three static routes and two dynamic routes have been included in the script
  *    The routes include **precipitation route, stations route, tobs route, start route and start/end route**
  *    Flask has been used
  *    All resusable code is defined before defining the routes

# Assumptions: 
* For retreiving the date one year from last date in dataset, it was advised not to use date as a variable. **I have provided alternate methods in comment section using hard coded date from previous steps** **date_clc = dt.datetime(2017, 8, 23)** however, using date generated into the variable from previous step is a better coding practice hence used that in my code. I have checked and both provide identical results
* We can use dropna from the dataframe. I tried both ways and on plotting the result was same so did not drop NA since it would involve additional work on x axis
* For station analysis, we could use last 12 months date from most recent date as calculated for previous line graph however, I have used 12 months of temperature data for the most active station based on the most recent date available for that station in the jupyter notebook code. It yields identical plots since there is a difference of only 1 row of data. Again I have not hard coded dates since its not a good coding practice. I havent hard coded staion id either
* Similar date calulations have been followed in the app.py script as well with alternate code in comments after checking both work correctly. I have dropped NA values in this case to display only available data in json format
* All details of stations from the measurements table have been extracted from the stations table for the stations route assuming all informaiton needs to be displayed for this route 
* In the dynamic routes we could have used error handling to determine correctness of date format inputted in URL. Current code would only output null

# References:
* https://stackoverflow.com/questions/33458566/how-to-choose-bins-in-matplotlib-histogram
* https://stackoverflow.com/questions/5219970/how-to-convert-string-to-datetime-in-python
* https://stackoverflow.com/questions/54446080/how-to-keep-order-of-sorted-dictionary-passed-to-jsonify-function#:~:text=The%20solution%20to%20set%20app.config%20%5B%27JSON_SORT_KEYS%27%5D%20%3D%20False,the%20sort_keys%20attribute%20on%20the%20app%27s%20JSONProvider%20instance%3A
  
