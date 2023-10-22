from database_connector import create_connection, close_connection
from database_records import  Skills_records
from db_functions import *

# Create a database connection
db_connection = create_connection()

# Create a cursor
mycursor = db_connection.cursor()

# Select the database
mycursor.execute("USE Database_python")

skills_table_definition = """
    CREATE TABLE IF NOT EXISTS Skills (
        skillID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        category ENUM('Frameworks', 'Tools', 'Coding Language', 'Methodology') NOT NULL,
        proficiency_level VARCHAR(50) NOT NULL,
        years_of_experience INT NOT NULL CHECK (years_of_experience > 0)
    )
"""


drop_and_create_table(mycursor, "Skills", skills_table_definition)
sql_skills_query = "INSERT INTO Skills (name, category, proficiency_level, years_of_experience) VALUES (%s, %s, %s, %s)"
insert_data(mycursor, Skills_records, sql_skills_query)

# Commit the changes to make them permanent
db_connection.commit()

# Fetch and print the results of the "Skills" table - FOR TESTING ONLY
mycursor.execute("SELECT * FROM Skills")
print("\nData in Skills Table:")
for x in mycursor:
    print(x)

# Close the cursor and connection
mycursor.close()
close_connection(db_connection)

