from typing import List

from api.models.dynamic_query_params import FilterCondition
from api.models.dynamic_query_params import QueryParameters
from core.config import settings
from core.db import engine
from core.db import get_db
from core.db import metadata
from core.security import request_limiter
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

query_route = APIRouter(prefix="/query")
limiter = request_limiter.get_limiter()


@query_route.post("/execute")
@limiter.limit("60/minute")
async def execute_query(
    request: Request,
    params: QueryParameters,
    db: Session = Depends(get_db),
):
    """
    Execute a dynamic query based on the provided parameters.
    """
    try:
        table = get_table(params.table_name, params.db_schema)
        query = build_select_query(table, params)

        results = db.execute(query).fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="Query results not found")

        return format_results(results, params.select_fields, table)
        
    except Exception as e:
        settings.logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


def get_table(table_name: str, db_schema: str | None = None):
    """
    Retrieve the SQLAlchemy Table object based on the table name and schema.
    """
    try:
        return Table(table_name, metadata, schema=db_schema, autoload_with=engine)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")


def build_select_query(table: Table, params: QueryParameters):
    """
    Build the SELECT query based on the provided parameters.
    """
    selected_columns = [table.c[field] for field in params.select_fields]
    query = select(*selected_columns)

    if params.filters:
        query = apply_filters(query, table, params.filters)

    if params.sort_by:
        query = apply_sorting(query, table, params.sort_by, params.sort_order)

    return query


def apply_filters(query, table: Table, filters: List[FilterCondition] | None = None):
    """
    Apply filters to the query based on the provided filter conditions.
    """
    conditions = []
    for filter_ in filters:
        column = table.c[filter_.field]
        condition = build_filter_condition(column, filter_)
        conditions.append(condition)

    return query.where(and_(*conditions))


def build_filter_condition(column, filter_: FilterCondition):
    """
    Build a single filter condition based on the filter operator.
    """
    if filter_.operator == "eq":
        return column == filter_.value
    elif filter_.operator == "ne":
        return column != filter_.value
    elif filter_.operator == "in":
        if isinstance(filter_.value, list):
            return column.in_(filter_.value)
        else:
            raise HTTPException(
                status_code=400, detail="For 'in' operator, the value must be a list."
            )
    else:
        raise_invalid_operator(filter_.operator)


def raise_invalid_operator(operator: str = ""):
    """
    Raise an HTTP exception for unsupported or missing operators.
    """
    if not operator:
        message = "Missing or empty operator. Please provide 'eq', 'ne', or 'in'."
    else:
        message = f"Unsupported operator: '{operator}'. Please use 'eq', 'ne', or 'in'."
    raise HTTPException(status_code=400, detail=message)


def apply_sorting(query, table: Table, sort_by: str, sort_order: str):
    """
    Apply sorting to the query based on the sort_by field and sort_order.
    """
    sort_column = table.c[sort_by]
    sort_func = asc if sort_order == "asc" else desc
    return query.order_by(sort_func(sort_column))


def format_results(results, select_fields, table: Table):
    """
    Format the results of the query into a list of dictionaries.
    """
    column_names = [table.c[field].name for field in select_fields]
    return [dict(zip(column_names, row)) for row in results]
