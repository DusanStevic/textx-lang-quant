from os import mkdir
from os.path import exists, dirname, join
import jinja2
import psycopg2
from psycopg2 import Error
import copy

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

# Generate report.html file
with open(join(srcgen_folder, "report.html"), 'w') as f:
    f.write(template.render(columns=columns,rows=rows))

