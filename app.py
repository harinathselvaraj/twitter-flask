from flask import Flask, render_template, send_file
# import pandas as pd
# from sqlalchemy import create_engine
# import numpy as np
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


# def get_data():
#     # engine = create_engine("mysql+pymysql://salutemuser:salutempasswd@localhost/salutemDB")    
#     engine = create_engine("mysql+pymysql://root:root@localhost/PYTHON_DB")    
#     drugs = pd.read_sql_query("select * from scraped", engine)
#    #  drugs['rr_start'] = drugs['rr_start'].apply(pd.to_datetime)
#    #  drugs['rr_end'] = drugs['rr_end'].apply(pd.to_datetime)
#    #  drugs['eu_market'] = drugs['eu_market'].apply(pd.to_datetime)
#    #  drugs['earliest'] = drugs['earliest'].apply(pd.to_datetime)
#    #  drugs['latest'] = drugs['latest'].apply(pd.to_datetime)

#     drugs['rr_start'] =  pd.to_datetime(drugs['rr_start'], format='%Y-%m-%d')
#     drugs['rr_end'] =  pd.to_datetime(drugs['rr_end'], format='%Y-%m-%d')
#     drugs['earliest'] =  pd.to_datetime(drugs['earliest'], format='%Y-%m-%d')
#     drugs['latest'] =  pd.to_datetime(drugs['latest'], format='%Y-%m-%d')
#     drugs['eu_market'].fillna('2000-01-01', inplace=True)    
#     drugs['eu_market'] =  pd.to_datetime(drugs['eu_market'], format='%Y-%m-%d')
#     drugs['rr_outcome'] = drugs['rr_outcome'].str.lower().str.replace('.','').str.replace('\n','').str.replace('a full','full').str.strip()

#     return drugs

@app.route("/rawdata")
def get_dataframe():
    drugs = get_data()
    return drugs.head().to_html()

if __name__ == '__main__':
    app.run(debug=True)

