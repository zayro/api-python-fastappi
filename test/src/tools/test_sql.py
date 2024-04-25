import pytest
from unittest.mock import MagicMock
from src.tools.sql import SqlTools


@pytest.fixture
def sql_tools():
    database = MagicMock()
    return SqlTools(database)


def test_select(sql_tools):
    table = "users"
    fields = ["id", "name", "email"]
    where = {"age": 25, "city": "New York"}
    order = {"name": "ASC"}
    limit = 10

    expected_query = "SELECT id, name, email FROM users WHERE age='25' AND city='New York' ORDER BY name ASC LIMIT 10;"
    actual_query = sql_tools.select(table, fields, where, order, limit)

    assert actual_query == expected_query


def test_generate_insert_query(sql_tools):
    table = "users"
    data = {"name": "John Doe", "email": "john@example.com"}

    expected_query = (
        "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');"
    )

    actual_query = sql_tools.generate_insert_query(table, data)

    assert actual_query == expected_query


def test_filter(sql_tools):
    table = "users"
    fields = ["id", "name", "email"]
    kwargs = {"age": 25, "city": "New York"}

    expected_query = (
        "SELECT id, name, email FROM users WHERE age='25' AND city='New York';"
    )
    actual_query = sql_tools.filter(table, fields, **kwargs)

    assert actual_query == expected_query


def test_generate_insert_query_multiple(sql_tools):
    table = "users"
    data = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
    ]

    expected_query = "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com'), ('Jane Smith', 'jane@example.com');"
    actual_query = sql_tools.generate_insert_query_multiple(table, data)

    assert actual_query == expected_query


def test_generate_insert_query_multiple_single_dict(sql_tools):
    table = "users"
    data = {"name": "John Doe", "email": "john@example.com"}

    expected_query = (
        "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');"
    )
    actual_query = sql_tools.generate_insert_query_multiple(table, data)

    assert actual_query == expected_query
