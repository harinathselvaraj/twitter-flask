from flask import Flask, render_template, send_file
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import pymysql
import TwitterMySQLserver
# import datetime
# import matplotlib.pyplot as plt
# import seaborn as sns
# import altair as alt


app = Flask(__name__)


@app.route("/")
def default():
    return render_template("home.html")


@app.route('/hello')
def hello():
   return "Hello from my web application."

@app.route('/start')
def start():
   TwitterMySQLserver.start()
   return render_template("home.html")
#    return "Loading tweets..Please wait for 5 seconds"

def get_data():
    engine = create_engine("mysql+pymysql://twitterusr:twitterpwd@321@166.62.26.1/harrytwitterdb")    
    twitterdata = pd.read_sql_query("select * from twitterdata", engine)
   #  drugs['rr_start'] = drugs['rr_start'].apply(pd.to_datetime)
    # drugs['eu_market'] =  pd.to_datetime(drugs['eu_market'], format='%Y-%m-%d')
    # drugs['rr_outcome'] = drugs['rr_outcome'].str.lower().str.replace('.','').str.replace('\n','').str.replace('a full','full').str.strip()

    return twitterdata

@app.route("/data")
def get_dataframe():
    twitterdata = get_data()
    # return twitterdata.head().to_html()
    return twitterdata.to_html()

if __name__ == '__main__':
    app.run(debug=True)

