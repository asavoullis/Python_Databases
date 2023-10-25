import pytest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from database_connector import create_connection, close_connection

# pytest test_database_connector.py

# patch creates a mock object
@pytest.fixture
def mock_db_config():
    return {
        'host': 'test_host',
        'user': 'test_user',
        'password': 'test_password',
        'port': 'test_port',
    }

@patch('database_connector.read_db_config')
# file.library.function
@patch('database_connector.mysql.connector.connect')
def test_create_connection(mock_connect, mock_read_db_config, mock_db_config):
    mock_read_db_config.return_value = mock_db_config
    create_connection()
    mock_connect.assert_called_once_with(
        host=mock_db_config['host'],
        user=mock_db_config['user'],
        password=mock_db_config['password'],
        port=mock_db_config['port']
    )

@patch('mysql.connector.connect')
def test_create_connection_exception(mock_connect, caplog):
    mock_connect.side_effect = Exception("Section MySQL not found in the database_config.ini file")
    with pytest.raises(Exception, match="Section MySQL not found in the database_config.ini file"):
        create_connection()
    assert "Error establishing database connection" in caplog.text


@patch('mysql.connector.connect')
def test_close_connection(mock_connect):
    connection_mock = mock_connect.return_value
    close_connection(connection_mock)
    connection_mock.close.assert_called_once()

@patch('mysql.connector.connect')
def test_close_connection_exception(mock_connect):
    connection_mock = mock_connect.return_value
    connection_mock.close.side_effect = Exception("Test Close Connection Error")
    with pytest.raises(Exception, match="Test Close Connection Error"):
        close_connection(connection_mock)

