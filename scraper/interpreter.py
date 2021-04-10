import time
import datetime
import pandas as pd
from sqlalchemy import create_engine
from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

this_folder = dirname(__file__)
grammar_folder = join(this_folder, 'grammar')
models_folder = join(this_folder, 'models')
# Get meta-model from language description
scraper_metamodel = metamodel_from_file(join(grammar_folder, 'scraper.tx'), debug=False)
# Instantiate model
scraper_model = scraper_metamodel.model_from_file(join(models_folder, 'query.scrp'))

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
print(df)
# PostgreSQL credentials
# engine = create_engine('postgresql://user:password@localhost/database_name')
engine = create_engine('postgresql://postgres:root@localhost/dsl')
con = engine.connect()
table_name = 'stocks'
df.to_sql(table_name, con, if_exists='replace', index='False')
con.close()




    

    
