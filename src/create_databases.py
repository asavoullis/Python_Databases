from database_connector import create_connection, close_connection
from database_records import Person_records, Skills_records

# Create a database connection
db_connection = create_connection()

# Create a cursor
mycursor = db_connection.cursor()

# Select the database
mycursor.execute("USE Database_python")

# Create or drop the "Person" table
table_name = "Person"
mycursor.execute(f"SHOW TABLES LIKE '{table_name}'")
table_exists = mycursor.fetchone()

if table_exists:
    mycursor.execute(f"DROP TABLE {table_name}")
    print(f"The table {table_name} has been dropped.")
else:
    print(f"The table {table_name} does not exist.")

# Creating the "Person" table
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Person (
        personID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        age SMALLINT UNSIGNED NOT NULL,
        gender ENUM('male', 'female') NOT NULL,
        created_date datetime NOT NULL,
        favouriteFood VARCHAR(255) NOT NULL
    )
""")

# Print "Person" table description
mycursor.execute("DESCRIBE Person")
print("Person Table Description:")
for row in mycursor:
    print(row)
print("")

# Insert data into the "Person" table
sql_person_query = "INSERT INTO Person (name, age, gender, created_date, favouriteFood) VALUES (%s, %s, %s, %s, %s)"

for person_data in Person_records:
    mycursor.execute(sql_person_query, person_data)


# Create or drop the "Person" table
table_name = "Skills"
mycursor.execute(f"SHOW TABLES LIKE '{table_name}'")
table_exists = mycursor.fetchone()

if table_exists:
    mycursor.execute(f"DROP TABLE {table_name}")
    print(f"The table {table_name} has been dropped.")
else:
    print(f"The table {table_name} does not exist.")


mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Skills (
        skillID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        category VARCHAR(255),
        proficiency_level VARCHAR(50),
        years_of_experience INT
    )
""")


mycursor.execute("DESCRIBE Skills")

# Fetch and print the results of the "Person" table description
print("Skills Table Description:")
for row in mycursor.fetchall():
    print(row)
print("")

# Insert data into the "Skills" table
sql_skills_query = "INSERT INTO Skills (name, category, proficiency_level, years_of_experience) VALUES (%s, %s, %s, %s)"

for skills_data in Skills_records:
    mycursor.execute(sql_skills_query, skills_data)

# Commit the changes to make them permanent
db_connection.commit()

# Fetch and print the results of the "Person" table
mycursor.execute("SELECT * FROM Person")
print("\nData in Person Table:")
for x in mycursor:
    print(x)

mycursor.execute("SELECT * FROM Skills")
print("\nData in Skills Table:")
for x in mycursor:
    print(x)

# Close the cursor and connection
mycursor.close()
close_connection(db_connection)
