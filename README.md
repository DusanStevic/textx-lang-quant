# Quant DSL 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## Introduction
Quant is a domain-specific language (DSL) for acquiring and visualizing financial time series.

This language was created during the Domain-Specific Languages course at the Faculty of Technical Sciences, University of Novi Sad.

## Domain
<p align="justify">
    Quant language is used in the financial domain particularly in the stock markets. Stock prices change every day by market forces. The law of supply and demand affects the stock market. If demand for stocks is higher than supply, then the price moves up and vice versa. When supply exceeds demand for stocks, prices fall. In order to gain some profit, it is important to have the right data. This is the time when Quant language comes to the scene.
Quant language is used as a tool for financial data science. It collects structured stock market data in form of financial time series. Financial time series represent stock price movements during the time. Quant language also provides financial time series visualization. Acquiring and visualizing financial time series is very important for investment decision-makers because these pieces of information have a huge impact on profitability.
</p>


# Data source
https://finance.yahoo.com
# Web Scraping Frameworks (Data acquisition modular)
![Web Scraping Frameworks](https://res.cloudinary.com/djxkexzcr/image/upload/v1611055729/DSL/Web_Scraping_Frameworks_fm0ksp.png "Web Scraping Frameworks")
![Data acquisition](https://res.cloudinary.com/djxkexzcr/image/upload/v1611058593/DSL/Data_acquisition_taapgm.png "Data acquisition")
# Stock markets reports (Data visualization boilerplate)
![Stock markets reports](https://res.cloudinary.com/djxkexzcr/image/upload/v1611058472/DSL/Stock_markets_reports_s1cfu7.png "Stock markets reports")
# Project flow
![Project flow](https://res.cloudinary.com/djxkexzcr/image/upload/v1611057271/DSL/Project_flow_lr6rtv.png "Project flow")

## Prerequisites
- [Python 3.7+](https://www.python.org/downloads/)
- [textX](https://github.com/textX/textX)
- [Graphviz](http://graphviz.org)
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)
- [Jinja2 template engine](https://jinja.palletsprojects.com/en/3.0.x/)
- [PostgreSQL](https://www.postgresql.org)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [pgAdmin](https://www.pgadmin.org)
- [Chart.js](https://www.chartjs.org)

## Instructions
Install instructions:
```
Install Python 3.7+
Install Graphviz
Install wkhtmltopdf
Install PostgreSQL
Install pgAdmin
```
pgAdmin and PostgreSQL database instructions:
```
Open pgAdmin, create PostgreSQL database, and remember database credentials:
db_name
db_user
db_password
```
Python environment instructions:
```
$ git clone https://github.com/DusanStevic/textx-lang-quant.git
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
Quant language instructions:
```
$ pip install -e textx-lang-quant
```
Check models and meta-models for syntax and semantic validity instructions:
```
$ textx check scraper.tx
$ textx check query.scrp --grammar scraper.tx
$ textx check report.tx
$ textx check report.rprt --grammar report.tx
```
List registered languages and generators instructions:
```
$ textx list-languages
$ textx list-generators
```
![List registered languages and generators](https://res.cloudinary.com/djxkexzcr/image/upload/v1624357391/DSL/generators_and_languages_zpg9ct.png)

## Usage
Scrape stock market data from Yahoo Finance API. Save scraped data to PostgreSQL database:
```
$ python interpreter.py path/to/*.scrp db_name db_user db_password
```
Call registered generators and transform given models to other target languages. Generate your stock market report:
```
$ textx generate --target html+pdf path/to/*.rprt
```
Visualize models and meta-models by generating visualizations:
```
$ python visualizator.py path/to/*.scrp
$ python visualizator.py path/to/*.rprt
```
## Contributors
- [Dušan Stević](https://github.com/DusanStevic)

## License
This project is licensed under the terms of the MIT license.
