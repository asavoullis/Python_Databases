from database_connector import create_connection, close_connection
from database_records import Person_records, Skills_records

def drop_and_create_table(mycursor, table_name, table_definition):
    mycursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    table_exists = mycursor.fetchone()

    if table_exists:
        mycursor.execute(f"DROP TABLE {table_name}")
        print(f"The table {table_name} has been dropped.")
    
    mycursor.execute(table_definition)

def print_table_description(mycursor, table_name):
    mycursor.execute(f"DESCRIBE {table_name}")
    print(f"{table_name} Table Description:")
    for row in mycursor.fetchall():
        print(row)
    print("")

def insert_data(mycursor, records, insert_query):
    for record_data in records:
        mycursor.execute(insert_query, record_data)

# Create a database connection
db_connection = create_connection()

# Create a cursor
mycursor = db_connection.cursor()

# Select the database
mycursor.execute("USE Database_python")

# Define table definitions
person_table_definition = """
    CREATE TABLE IF NOT EXISTS Person (
        personID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        age SMALLINT UNSIGNED NOT NULL,
        gender ENUM('male', 'female') NOT NULL,
        created_date datetime NOT NULL,
        favouriteFood VARCHAR(255) NOT NULL
    )
"""

skills_table_definition = """
    CREATE TABLE IF NOT EXISTS Skills (
        skillID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        category ENUM('Frameworks', 'Tools', 'Coding Language', 'Methodology') NOT NULL,
        proficiency_level VARCHAR(50) NOT NULL,
        years_of_experience INT NOT NULL CHECK (years_of_experience > 0)
    )
"""

# Drop if exists and re-create the "Person" table
drop_and_create_table(mycursor, "Person", person_table_definition)

# Print "Person" table description - FOR TESTING ONLY
print_table_description(mycursor, "Person")

# Insert data into the "Person" table
sql_person_query = "INSERT INTO Person (name, age, gender, created_date, favouriteFood) VALUES (%s, %s, %s, %s, %s)"
insert_data(mycursor, Person_records, sql_person_query)


drop_and_create_table(mycursor, "Skills", skills_table_definition)
print_table_description(mycursor, "Skills") # - FOR TESTING ONLY
sql_skills_query = "INSERT INTO Skills (name, category, proficiency_level, years_of_experience) VALUES (%s, %s, %s, %s)"
insert_data(mycursor, Skills_records, sql_skills_query)

# Commit the changes to make them permanent
db_connection.commit()

# Fetch and print the results of the "Person" table
mycursor.execute("SELECT * FROM Person")
print("\nData in Person Table:")
for x in mycursor:
    print(x)

# Fetch and print the results of the "Skills" table
mycursor.execute("SELECT * FROM Skills")
print("\nData in Skills Table:")
for x in mycursor:
    print(x)

# Close the cursor and connection
mycursor.close()
close_connection(db_connection)
