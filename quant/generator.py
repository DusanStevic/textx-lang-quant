import sys
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
from textx import metamodel_from_file
import datetime
# Set wkhtmltopdf Path variable
os.environ["PATH"] += os.pathsep + 'C:/Program Files/wkhtmltopdf/bin'


def generate(model):
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
        # Get stock market ticker from pandas DataFrame
        ticker = df['Ticker'][0]
        # Start of time serie
        start = df['Date'][0]
        # End of time serie
        end = df['Date'][len(df.index)-1]
            
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

    grammars_folder = join(this_folder, 'grammars')
    # Get meta-model from language description
    report_metamodel = metamodel_from_file(join(grammars_folder, 'reporter.tx'), debug=False)
    # Instantiate model. Examples folder contains reporter models with file extension .rprt
    report_model = report_metamodel.model_from_file(model)
    # Initialize template engine.
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_folder),trim_blocks=True,lstrip_blocks=True)
    # Generate report.html file
    with open(join(srcgen_folder, "report.html"), 'w') as f:
        for details in report_model.report.details:
            if(details.report_details_type == "general"):
                topic = details.topic
                source = details.source
                source_name = details.source_name
                creator = details.creator
                now = "Creation date not provided"
                if(details.creation_date == True):
                    now = datetime.datetime.now().strftime("%A, %B %d, %Y %X")
                logo_source = details.fields[0].value
                logo = details.fields[1].value
                logo_name = details.fields[2].value
                # Load general template
                template = jinja_env.get_template('GeneralDetails.j2')
                f.write(template.render(topic=topic, source=source, source_name=source_name, 
                now=now, creator=creator, logo_source=logo_source, logo=logo, logo_name=logo_name))
            elif(details.report_details_type == "tabular"):
                topic = details.topic
                source = details.source
                source_name = details.source_name
                border = "0"
                if(details.fields[0].value == True):
                    border = "1"
                # Load tabular template              
                template = jinja_env.get_template('TabularDetails.j2')
                f.write(template.render(topic=topic, source=source, source_name=source_name,
                border=border, columns=columns, rows=rows, ticker=ticker, start=start, end=end))

            elif(details.report_details_type == "graphical"):
                topic = details.topic
                source = details.source
                source_name = details.source_name
                # Dates for time series
                labels=json.dumps(df["Date"].tolist())
                # Generate time series using Date column and one of the following columns: Open, High, Low, Close, Adj Close, or Volume.
                time_series_column = details.fields[0].value
                data = json.dumps(df[time_series_column].tolist())
                currency = details.fields[1].value
                # Load graphical template
                template = jinja_env.get_template('GraphicalDetails.j2')
                f.write(template.render(topic=topic, source=source, source_name=source_name, 
                data=data, labels=labels, ticker=ticker, time_series_column=time_series_column,
                currency=currency))
            elif(details.report_details_type == "pictorial"):
                topic = details.topic
                source = details.source
                source_name = details.source_name
                picture = details.fields[0].value
                width = details.fields[1].value
                height = details.fields[2].value
                align = details.fields[3].value
                # Load pictorial template
                template = jinja_env.get_template('PictorialDetails.j2')
                f.write(template.render(topic=topic, source=source, source_name=source_name,
                picture=picture, width=width, height=height, align=align))
            elif(details.report_details_type == "textual"):
                topic = details.topic
                source = details.source
                source_name = details.source_name
                text = details.fields[0].value
                font = details.fields[1].value
                size = details.fields[2].value
                color = details.fields[3].value
                align = details.fields[4].value
                # Load textual template
                template = jinja_env.get_template('TextualDetails.j2')
                f.write(template.render(topic=topic, source=source, source_name=source_name,
                text=text, font=font, size=size, color=color, align=align))
            else:
                print("Minimum one report detail is required. Please add report details and try again.")

    # Generate report.pdf file from report.html file (wkhtmltopdf utility to convert HTML to PDF using Webkit)
    pdfkit.from_file(join(srcgen_folder, "report.html"), join(srcgen_folder, "report.pdf"))

