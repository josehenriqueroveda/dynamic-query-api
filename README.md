# Dynamic Query API
This project is an API built with FastAPI that allows dynamic query execution on a PostgreSQL database. The API enables users to dynamically define select fields, table, filters, sorting, and database schema to flexibly query data.

## Features
- Select specific fields from a table.
- Dynamic filtering with operators `(eq, ne, in)`.
- Sorting by field and order `(asc or desc)`.
- Support for different database schemas.


## Technologies Used
- Python 3.10+
- **FastAPI** - A modern, fast web framework for building APIs with Python.
- **SQLAlchemy** - ORM for interacting with PostgreSQL databases.
- **Pre-commit** - A tool for managing and enforcing the quality of Python code.

## Endpoints
```http
POST /api/v1/query/execute
```
Executes a dynamic query on the database.

Example Request
```
curl -X 'POST' \
  'http://localhost:32809/api/v1/query/execute' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "select_fields": ["product", "descripton", "price"],
  "table_name": "products",
  "db_schema": "stage",
  "sort_by": "price",
  "sort_order": "desc",
  "filters": [
    {
      "field": "category",
      "operator": "eq",
      "value": "eletronics"
    }
  ]
}'
```

**Parameters**
- `select_fields`: List of fields to select from the table.
- `table_name`: The name of the table to query.
- `db_schema`: (Optional) Database schema.
- `sort_by`: (Optional) Field to sort by.
- `sort_order`: (Optional) Sort order (asc or desc).
- `filters`: (Optional) List of filter conditions. Each filter contains:
- `field`: Name of the field.
- `operator`: Comparison operator (eq, ne, in).
- `value`: Value to compare.


To run with Uvicorn:

```bash
uvicorn agro_navi.main:app --port 32809 --reload
# Choose the port you want to use (32809 is just an example)
```
Access the interactive API documentation at: `http://localhost:32809/docs`

Pre-commit hooks:

```bash
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
```