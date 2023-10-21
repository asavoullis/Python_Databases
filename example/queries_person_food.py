import sys
import os

# Get the current script's directory
current_script_directory = os.path.dirname(os.path.realpath(__file__))

# Add the "src" directory to the Python path
src_directory = os.path.join(current_script_directory, "..", "src")
sys.path.append(src_directory)

from database_connector import create_connection, close_connection
from db_functions import *


""" 
Run this script from the src directory 
python ../example/queries_person_food.py 
"""



# Create a database connection
db_connection = create_connection()

# Create a cursor
mycursor = db_connection.cursor()

# Select the database
mycursor.execute("USE Database_python")


# Modify the query according to your needs
query = """
    SELECT Person.personID, Person.name, Person.age, Food.foodname
    FROM Person
    INNER JOIN Food ON Person.favouriteFood = Food.food_id
    WHERE Person.age > %s
"""

params = (18,)  
result = execute_query(mycursor, query, params)

# Process the result as needed
if result is not None:
    for row in result:
        print(row)
else:
    print("No results found.")



# Close the cursor and connection
mycursor.close()
close_connection(db_connection)
