from flask import Flask, render_template, send_file
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


app = Flask(__name__)


@app.route("/")
def default():
    return render_template("home.html")


@app.route('/hello')
def hello():
   return "Hello from my web application."


def get_data():
    # engine = create_engine("mysql+pymysql://salutemuser:salutempasswd@localhost/salutemDB")    
    engine = create_engine("mysql+pymysql://root:root@localhost/PYTHON_DB")    
    drugs = pd.read_sql_query("select * from scraped", engine)
   #  drugs['rr_start'] = drugs['rr_start'].apply(pd.to_datetime)
   #  drugs['rr_end'] = drugs['rr_end'].apply(pd.to_datetime)
   #  drugs['eu_market'] = drugs['eu_market'].apply(pd.to_datetime)
   #  drugs['earliest'] = drugs['earliest'].apply(pd.to_datetime)
   #  drugs['latest'] = drugs['latest'].apply(pd.to_datetime)

    drugs['rr_start'] =  pd.to_datetime(drugs['rr_start'], format='%Y-%m-%d')
    drugs['rr_end'] =  pd.to_datetime(drugs['rr_end'], format='%Y-%m-%d')
    drugs['earliest'] =  pd.to_datetime(drugs['earliest'], format='%Y-%m-%d')
    drugs['latest'] =  pd.to_datetime(drugs['latest'], format='%Y-%m-%d')
    drugs['eu_market'].fillna('2000-01-01', inplace=True)    
    drugs['eu_market'] =  pd.to_datetime(drugs['eu_market'], format='%Y-%m-%d')
    drugs['rr_outcome'] = drugs['rr_outcome'].str.lower().str.replace('.','').str.replace('\n','').str.replace('a full','full').str.strip()

    return drugs

@app.route('/dataviz')
def display_dataviz():
    drugs = get_data()
    df = drugs

    #viz 1
    viz1 = alt.Chart(df).mark_bar(color='green').encode(
    x= alt.X('ncpe_year'),
    y= 'count()')
    viz1.save('static/images/1.png')

    #viz 2
    sns.set(style="whitegrid")
    ta_list_count  = df['ta_list'].value_counts()
    ta_list_count = ta_list_count[:6,]
    ta_list_count = ta_list_count.drop('Unknown')
    plt.figure(figsize=(11,8))
    sns.barplot(ta_list_count.values, ta_list_count.index, alpha=1,palette=("Paired"))
    plt.title('Top 5 Common diseases for which medicines were submitted to NCPE', fontsize=22)
    plt.xlabel('Number of Occurrences', size="20")
    plt.ylabel('Disease Type', size="20")
    plt.savefig('static/images/2.png')

    #viz 3
    company_count = df['company'].value_counts()[:8] #Top 8 companies
    top_others_company_count = df['company'].value_counts()[8:] #Rest of the Companies
    #Taking the Sum of counts of other companies and adding as 'Others' to the series
    sum_of_others = np.sum(top_others_company_count.values)
    s1 = pd.Series([sum_of_others], index=['Others'])
    company_count = company_count.append(s1)
    company_count = company_count.drop('Unknown') #dropping 'Unknown' company name
    #Plotting the company-wise percentage of drugs in NCPE Database
    labels = company_count.index
    sizes = company_count.values
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig('static/images/3.png')


    #viz 4
    df['rr_outcome_type'] = ~df['rr_outcome'].str.contains('not recommended')
    df['rr_outcome_type'] = df['rr_outcome_type'].replace(False,'Not Recommended').replace(True,'Recommended')
    df2 = df.groupby(['ncpe_year','rr_outcome_type'])['ncpe_year'].count().unstack('rr_outcome_type').fillna(0)
    df2.plot(kind='bar', stacked=True, color=['red', 'green'])
    plt.savefig('static/images/4.png')


    #viz 5
    rr_status = alt.Chart(df).mark_point().encode(
      x='rr_status',
      y='count()',
      color='rr_status',).properties(
      width=500,
      height=250
      ).interactive()
    rr_status.save("static/images/5.png")

    return ('''
    
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <title>Python Data Visualizations</title>
  </head>
  <body>
	  
<div class="container col-md-10">

    <h1 class="mt-5">Data visualizations</h1>
    <div style="border-top: 4px solid blue;"></div>

    <h4 class="mt-4">1. View the Amount of Drugs registered Year-wise in NCPE Website</h4> 
    <img src="static/images/1.png">
    <div class="clearfix"></div>
    <strong>Reason for Visualization 1:</strong>
    <p>This graph is important since it provides a rough idea of how many drugs were present in NCPE database for all the years. </p>
    <strong>Information obtained from Visualization 1:</strong>
    <p>It is observed that the No.of drugs were inreasing from 2004 to 2018. There is a slight decrease in the year - 2016. The year - 2018 has highest number of drugs found in NCPE Database</p>
    <div style="border-top: 4px solid blue;"></div>

    <h4 class="mt-4">2. Top 5 Medical Symptoms for which the manufacturers(pharamaceutical companies) had submitted their medicines for approval by NCPE</h4> 
    <img src="static/images/2.png">
    <div class="clearfix"></div>
    <strong>Reason for Visualization 2:</strong>
    <p>When I found the distinct entries in the column - 'ta_list', it looked like a disease names. So, I wanted to see the most common diseases for which the drugs were found in NCPE database. </p>
    <strong>Information obtained from Visualization 2:</strong>
    <p>On an overall basis, Many Companies have applied for liscence from NCPE for critical diseases such as Influenza, Radionuclide Imaging, Hepatitis followed by HIV Infections and Multiple Sclerosis. This conveys that those medicines were highly in demand and it led to the spike in the production of new medicines for those diseases and thereby obtain approval from NCPE</p>
    <div style="border-top: 4px solid blue;"></div>

    <h4 class="mt-4">3. Company-wise percentage of total drugs in NCPE Database</h4> 
    <img src="static/images/3.png">
    <div class="clearfix"></div>
    <strong>Reason for Visualization 3:</strong>
    <p>I wanted to see the distribution of pharameceutial companies found in NCPE database. This will help to understand the top companies which applied for NCPE liscence. </p>    
    <strong>Information obtained from Visualization 3:</strong>
    <p>This chart shows that 'Novartis' had the higest number of drugs submitted to NCPE followed by 'GlaxoSmithKline' and 'Pfizer'. Although, 'GlaxoSmithKline' and 'Pfizer' are large companies, they only contribute below 10% of the total drugs in NCPE Database. This denotes that there are many small players (about 58%) in the pharameceutial field who contribute less than 4.4% individually.</p>
    <div style="border-top: 4px solid blue;"></div>
    
    <h4 class="mt-4">4. Year-wise Comparision of RR Outcome Results</h4> 
    <img src="static/images/4.png">
    <div class="clearfix"></div>
    <strong>Reason for Visualization 4:</strong>
    <p>This is an important chart to understand what is the ratio of drugs that were approved/rejected by NCPE for various years.</p>
    <strong>Information obtained from Visualization 4:</strong>
    <p>Higher rejections are found in the years - 2011, 2013 and 2014. There is a gradual decrease in the number of rejections in the recent years. Pharamaceutical companies may have done rigorous tests (for their new drugs) in their labs before applying for NCPE liscence.</p>
    <div style="border-top: 4px solid blue;"></div>

    <h4 class="mt-4">5. Find the distribution of medicines in NCPE database according to 'rr_status'</h4> 
    <img src="static/images/5.png">
    <div class="clearfix"></div>
    <strong>Reason for Visualization 5:</strong>
    <p>This chart displays the ratio of 'rr_status' for all the drugs in the NCPE database. This helps us to identify the no.of drugs for each 'rr_status' an overall basis. </p>
    <strong>Information obtained from Visualization 5:</strong>
    <p>Maximum drugs belong to 'The HTA recommended at submitted price' (around 220 drugs) followed by 'No HTA' (120 drugs). There are few drugs that belong to 'RR not conducted' (30 drugs). Other statuses are very minimum compared to the above mentioned major ones.</p>

</div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  </body>
</html>

    ''')


@app.route("/rawdata")
def get_dataframe():
    drugs = get_data()
    return drugs.head().to_html()

if __name__ == '__main__':
    app.run(debug=True)

