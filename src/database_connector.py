import mysql.connector
from configparser import ConfigParser
import logging

# Function for database connection with error handling
def create_connection():
    try:
        def read_db_config(filename='database_config.ini', section='MySQL'):
            parser = ConfigParser()
            parser.read(filename)
            db_config = {}
            if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                    db_config[param[0]] = param[1]
            else:
                raise Exception(f"Section {section} not found in the {filename} file")
            return db_config

        db_config = read_db_config()
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )
        logging.info("Database connection established successfully.")
        return connection
    except Exception as e:
        logging.error(f"Error establishing database connection: {e}")
        raise

def close_connection(connection):
    try:
        connection.close()
        logging.info("Database connection closed successfully.")
    except Exception as e:
        logging.error(f"Error closing database connection: {e}")
        raise
