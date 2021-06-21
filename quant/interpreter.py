import sys
import time
import datetime
import pandas as pd
from sqlalchemy import create_engine
from os.path import join, dirname
from textx import metamodel_from_file

this_folder = dirname(__file__)
grammars_folder = join(this_folder, 'grammars')
# Get meta-model from language description
scraper_metamodel = metamodel_from_file(join(grammars_folder, 'scraper.tx'), debug=False)
# Instantiate model. Examples folder contains scraper models with file extension .scrp
scraper_model = scraper_metamodel.model_from_file(sys.argv[1])
# get ticker symbol from scraper model
ticker = scraper_model.query.details.ticker.symbol

# start date (period1) from scraper model
period1_year = int(scraper_model.query.details.start.start.year)
period1_month = int(scraper_model.query.details.start.start.month)
period1_day = int(scraper_model.query.details.start.start.day)
period1 = int(time.mktime(datetime.datetime(period1_year, period1_month, period1_day, 23, 59).timetuple())) 

# end date (period2) from scraper model
period2_year = int(scraper_model.query.details.end.end.year)
period2_month = int(scraper_model.query.details.end.end.month)
period2_day = int(scraper_model.query.details.end.end.day)
period2 = int(time.mktime(datetime.datetime(period2_year, period2_month, period2_day, 23, 59).timetuple())) 

# Frequency – Daily (1d), Weekly (1wk), Monthly (1mo)
# get interval from scraper model
interval = scraper_model.query.details.interval 
query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
df = pd.read_csv(query_string)
# Adding ticker column to existing DataFrame in Pandas (providing extra information)
ticker_column = []
for item in range(len(df.index)):
    ticker_column.append(ticker)
df['Ticker'] = ticker_column
# PostgreSQL credentials
# engine = create_engine('postgresql://user:password@localhost/database_name')
engine = create_engine('postgresql://postgres:root@localhost/dsl')
con = engine.connect()
table_name = 'stocks'
df.to_sql(table_name, con, if_exists='replace', index='False')
con.close()




    

    
