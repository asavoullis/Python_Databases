from datetime import datetime
from database_connector import create_connection, close_connection

# Create a database connection
db_connection = create_connection()

# Create a cursor
mycursor = db_connection.cursor()

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

# Create or drop the "Skills" table
table_name = "Skills"
mycursor.execute(f"SHOW TABLES LIKE '{table_name}'")
table_exists = mycursor.fetchone()

if table_exists:
    mycursor.execute(f"DROP TABLE {table_name}")
    print(f"The table {table_name} has been dropped.")
else:
    print(f"The table {table_name} does not exist.")

# Creating the "Skills" table
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Skills (
        skillID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        category VARCHAR(255),
        proficiency_level VARCHAR(50),
        years_of_experience INT
    )
""")

# Print "Skills" table description
mycursor.execute("DESCRIBE Skills")
print("Skills Table Description:")
for row in mycursor.fetchall():
    print(row)
print("")

# Insert data into the "Person" table
Person_records = [
    ("Tim", 19, "male", datetime.now().strftime('%Y-%m-%d'), "chicken"),
    ("Jake", 20, "male", datetime.now().strftime('%Y-%m-%d'), "beef"),
    ("Jack", 21, "male", datetime.now().strftime('%Y-%m-%d'), "lemon soup"),
    ("Joe", 32, "male", datetime.now().strftime('%Y-%m-%d'), "orange"),
    ("Maria", 22, "female", datetime.now().strftime('%Y-%m-%d'), "banana"),
    ("Kate", 35, "female", datetime.now().strftime('%Y-%m-%d'), "banana"),
    ("Daniel", 28, "male", datetime.now().strftime('%Y-%m-%d'), "tomato"),
    ("Jess", 45, "female", datetime.now().strftime('%Y-%m-%d'), "banana"),
]

sql_query = "INSERT INTO Person (name, age, gender, created_date, favouriteFood) VALUES (%s, %s, %s, %s, %s)"

for person_data in Person_records:
    mycursor.execute(sql_query, person_data)

# Commit the changes to make them permanent
db_connection.commit()

# Fetch and print the results of the "Person" table
mycursor.execute("SELECT * FROM Person")
print("\nData in Person Table:")
for x in mycursor:
    print(x)

# Close the cursor and connection
mycursor.close()
close_connection(db_connection)
