import json
import pandas as pd
from os import mkdir
from os.path import exists, dirname, join
import jinja2
import psycopg2
from psycopg2 import Error
import copy
import pdfkit
import os
# Set wkhtmltopdf Path variable
os.environ["PATH"] += os.pathsep + 'C:/Program Files/wkhtmltopdf/bin'

try:
    # Connect to an existing dsl database
    connection = psycopg2.connect(dbname="dsl", user="postgres", password="root")
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Executing a SQL query
    cursor.execute("SELECT * FROM stocks")
    # Fetch result
    rows_temp = cursor.fetchall()
    # Get the column names from a stocks table in dsl database
    columns_temp = []
    for column_name in cursor.description:
        columns_temp.append(column_name[0])
    # Drop the index column of a pandas DataFrame 
    columns = []
    # [1:]: skip the first element (skip index column)
    for column in columns_temp[1:]:
        columns.append(column)
    rows = []
    for row in rows_temp:
        row_temp = []
        # [1:]: skip the first element (skip index column)
        for cell in row[1:]:
            row_temp.append(cell)
        rows.append(copy.deepcopy(row_temp))
        row_temp.clear()
    # Use the pandas read_sql_query function to read 
    # the results of a SQL query directly into a pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM stocks", connection)
        

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()


this_folder = dirname(__file__)
templates_folder = join(this_folder, 'templates')
# Create output folder
srcgen_folder = join(this_folder, 'srcgen')
if not exists(srcgen_folder):
    mkdir(srcgen_folder)

# Initialize template engine.
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_folder),trim_blocks=True,lstrip_blocks=True)

# Load template
template = jinja_env.get_template('TabularDetails.j2')
template1 = jinja_env.get_template('GraphicalDetails.j2')
#data = json.dumps( [1.0,2.0,3.0] )
data = json.dumps(df["Close"].tolist())
#labels=json.dumps( ["18-12-31", "19-01-01", "19-01-02"] )
labels=json.dumps(df["Date"].tolist())
topic = "Yahoo Finance Charts"


# Generate report.html file
with open(join(srcgen_folder, "report.html"), 'w') as f:
    f.write(template.render(columns=columns,rows=rows))
    f.write(template1.render(data=data, labels=labels, topic=topic))
    
# Generate report.pdf file from report.html file (wkhtmltopdf utility to convert HTML to PDF using Webkit)
pdfkit.from_file(join(srcgen_folder, "report.html"), join(srcgen_folder, "report.pdf"))

print(df)
