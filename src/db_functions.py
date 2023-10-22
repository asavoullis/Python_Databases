
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
