import pytest
import logging
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from db_functions import drop_and_create_table, print_table_description, insert_data, execute_query


@patch('mysql.connector.connect')
def test_drop_and_create_table(mock_connect):
    # Create a mock cursor and connection
    mock_cursor = mock_connect.return_value.cursor.return_value

    table_name = 'test_table'
    table_definition = 'CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)'
    
    # Test dropping and creating a table
    drop_and_create_table(mock_cursor, table_name, table_definition)
    
    # Check if the test_table exists
    mock_cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = mock_cursor.fetchone()

    # Assert that the table exists
    assert result is not None, f"The table {table_name} does exist after drop_and_create_table"


@patch('mysql.connector.connect')
def test_print_table_description(mock_connect, caplog):
    # Create a mock cursor and connection
    mock_cursor = mock_connect.return_value.cursor.return_value

    table_name = 'test_table'

    # print_table_description(mock_cursor, table_name)
    # Test printing table description
    with caplog.at_level(logging.DEBUG):  # Capture logs at DEBUG level
        print_table_description(mock_cursor, table_name)

    # Add assertions based on your expectations
    assert "Table description for test_table printed successfully." in caplog.text

@patch('mysql.connector.connect')
def test_insert_data(mock_connect):
    # Create a mock cursor and connection
    mock_cursor = mock_connect.return_value.cursor.return_value


    records = [(1, 'John'), (2, 'Jane')]
    insert_query = 'INSERT INTO test_table (id, name) VALUES (%s, %s)'

    with patch.object(mock_cursor, 'execute') as mock_execute:
        insert_data(mock_cursor, records, insert_query)

        # assert that the cursor.execute method was called for each record
        assert mock_execute.call_count == len(records)


@patch('mysql.connector.connect')
def test_execute_query(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value

    query = 'SELECT * FROM test_table'
    params = (1,)

    mock_cursor.fetchall.return_value = [(1, 'John'), (2, 'Jane')]
    result = execute_query(mock_cursor, query, params)

    assert result == [(1, 'John'), (2, 'Jane')], "Unexpected result returned from execute_query"
    assert len(result) == 2, "Expected 2 rows of data, but got diffrent number"


@patch('mysql.connector.connect')
def test_execute_query2(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value

    query = 'SELECT * FROM test_table'
    params = (1,)
    # Set the expected return value when fetchall is called
    expected_data = [(1, 'John'), (2, 'Jane')]
    mock_cursor.fetchall.return_value = expected_data

    # Test executing a query
    result = execute_query(mock_cursor, query, params)

    # Add assertions based on your expectations
    mock_cursor.execute.assert_called_once_with(query, params)
    assert result == expected_data, f"Expected data: {expected_data}, Actual data: {result}"

    
@patch('mysql.connector.connect')
def test_execute_query3(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value

    query = 'SELECT * FROM test_table'
    params = (1,)

    # Test executing a query
    result = execute_query(mock_cursor, query, params)
    assert result is not None
