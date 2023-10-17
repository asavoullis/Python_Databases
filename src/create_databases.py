from database_connector import create_connection, close_connection
from database_records import Person_records, Food_records
from db_functions import * 

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
        favouriteFood MEDIUMINT ZEROFILL,
        FOREIGN KEY (favouriteFood) REFERENCES Food(food_id)
    )
"""

food_table_definition = """
    CREATE TABLE IF NOT EXISTS Food (
        food_id MEDIUMINT ZEROFILL PRIMARY KEY AUTO_INCREMENT,
        foodname VARCHAR(255) NOT NULL,
        calories_per_100g FLOAT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        weight INT NOT NULL,
        category VARCHAR(255) NOT NULL
    )
"""

# Fetch the foreign key constraint name dynamically
mycursor.execute("""
    SELECT CONSTRAINT_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_NAME = 'Person'
    AND REFERENCED_TABLE_NAME = 'Food'
""")
result = mycursor.fetchone()

# Check if a foreign key constraint was found
if result:
    foreign_key_name = result[0]
    print(f"Found foreign key constraint: {foreign_key_name}")

    # Drop the foreign key constraint
    mycursor.execute(f"ALTER TABLE Person DROP FOREIGN KEY {foreign_key_name}")
    print(f"The foreign key constraint {foreign_key_name} has been dropped.")

print_table_description(mycursor, "Person")
sql_person_query = "INSERT INTO Person (name, age, gender, created_date, favouriteFood) VALUES (%s, %s, %s, %s, %s)"
insert_data(mycursor, Person_records, sql_person_query)

print_table_description(mycursor, "Food")  # - FOR TESTING ONLY
sql_food_query = "INSERT INTO Food (foodname, calories_per_100g, price, weight, category) VALUES (%s, %s, %s, %s, %s)"
# Remove food_id from the query and each tuple in Food_records
Food_records = [(record[1], record[2], record[3], record[4], record[5]) for record in Food_records]
insert_data(mycursor, Food_records, sql_food_query)

# drop_and_create_table(mycursor, "Food", food_table_definition)
# drop_and_create_table(mycursor, "Person", person_table_definition)

# Commit the changes to make them permanent
db_connection.commit()

# Fetch and print the results of the "Person" table - FOR TESTING ONLY
mycursor.execute("SELECT * FROM Person")
print("\nData in Person Table:")
for x in mycursor:
    print(x)



# Fetch and print the results of the "Food" table - FOR TESTING ONLY
mycursor.execute("SELECT * FROM Food")
print("\nData in Food Table:")
for x in mycursor:
    print(x)

# Close the cursor and connection
mycursor.close()
close_connection(db_connection)
