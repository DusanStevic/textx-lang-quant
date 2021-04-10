import psycopg2
from psycopg2 import Error

try:
    # Connect to an existing dsl database
    connection = psycopg2.connect(dbname="dsl", user="postgres", password="root")
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT * FROM stocks")
    # Fetch result
    records = cursor.fetchall()
    print("You are connected to - ", records, "\n")
    for record in records:
        print(record)
    
    for name in cursor.description:
        print(name[0])

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")