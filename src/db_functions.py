import logging

def drop_and_create_table(mycursor, table_name, table_definition):
    mycursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    table_exists = mycursor.fetchone()

    if table_exists:
        try:
            mycursor.execute(f"DROP TABLE {table_name}")
            logging.info(f"The table {table_name} has been dropped.")
        except Exception as drop_error:
            logging.error(f"Error dropping table {table_name}: {drop_error}")
            raise

    try:
        mycursor.execute(table_definition)
        logging.info(f"The table {table_name} has been created.")
    except Exception as create_error:
        logging.error(f"Error creating table {table_name}: {create_error}")
        raise


def print_table_description(mycursor, table_name):
    try:
        mycursor.execute(f"DESCRIBE {table_name}")
        logging.debug(f"{table_name} Table Description:")
        for row in mycursor.fetchall():
            logging.debug(row)
        logging.debug("")
        logging.info(f"Table description for {table_name} printed successfully.")
    except Exception as e:
        logging.error(f"Error printing table description: {e}")
        raise


def insert_data(mycursor, records, insert_query):
    try:
        for record_data in records:
            mycursor.execute(insert_query, record_data)
        logging.info(f"Data inserted successfully using query: {insert_query}")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        raise


def execute_query(mycursor, query, params=None):
    try:
        if params:
            mycursor.execute(query, params)
        else:
            mycursor.execute(query)
        
        # Fetch all results before returning
        result = mycursor.fetchall()

        logging.info(f"Query executed successfully: {query}")
        return result
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        raise