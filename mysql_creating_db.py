import mysql.connector 
from configparser import ConfigParser

# Function to read database configuration from the INI file
def read_db_config(filename='database_config.ini', section='MySQL'):
    # Create a parser
    parser = ConfigParser()

    # Read the configuration file
    parser.read(filename)

    # Get the section, default to MySQL
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db_config

# Read database configuration from the INI file
db_config = read_db_config()

# Connect to MySQL using the configuration from the INI file
db = mysql.connector.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    port=db_config['port']
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Database_python")

# Select the newly created database
mycursor.execute("USE Database_python")

# Creating the "Person" table
# The triple double-quotes (""") are used to create multi-line strings in Python.
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Person (
        personID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        age SMALLINT UNSIGNED NOT NULL,
        favouriteFood VARCHAR(255) NOT NULL
    )
""")

print("")
mycursor.execute("DESCRIBE Person")
print("Person Table Description:")
for row in mycursor:
    print(row)
print("")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Skills (
        skillID INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255)
    )
""")

mycursor.execute("DESCRIBE Skills")

# Fetch and print the results of the "Person" table description
print("Skills Table Description:")
for row in mycursor.fetchall():
    print(row)
print("")


mycursor.execute("INSERT INTO Person (name, age, favouriteFood) VALUES (%s, %s, %s)", ("Tim", 19, "chicken"))
mycursor.execute("INSERT INTO Person (name, age, favouriteFood) VALUES (%s, %s, %s)", ("Jake", 20, "beef"))
mycursor.execute("INSERT INTO Person (name, age, favouriteFood) VALUES (%s, %s, %s)", ("Jack", 21, "lemon soup"))
mycursor.execute("INSERT INTO Person (name, age, favouriteFood) VALUES (%s, %s, %s)", ("Joe", 32, "orange"))
mycursor.execute("INSERT INTO Person (name, age, favouriteFood) VALUES (%s, %s, %s)", ("Daniel", 28, "tomatoe"))

# Commit the changes to make them permanent
db.commit()

mycursor.execute("SELECT * FROM Person")
for x in mycursor:
    print(x)


mycursor.close()
db.close()