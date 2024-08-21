from api.models.dynamic_query_params import DynamicQueryParams
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
    params: DynamicQueryParams,
    db: Session = Depends(get_db),
):
    """
    Execute a query.
    """

    try:

        table = Table(
            params.table, metadata, schema=params.schema, autoload_with=engine
        )
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")

    selected_columns = [table.c[field] for field in params.select_fields]
    query = select(*selected_columns)

    # Aplicar filtros
    if params.filters:
        conditions = []
        for filter_ in params.filters:
            column = table.c[filter_.field]
            if filter_.operator == "eq":
                conditions.append(column == filter_.value)
            elif filter_.operator == "ne":
                conditions.append(column != filter_.value)
            elif filter_.operator == "in":
                if isinstance(filter_.value, list):
                    conditions.append(column.in_(filter_.value))
                else:
                    raise HTTPException(
                        status_code=400, detail=f"Value for 'in' must be a list."
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Operator not supported: {filter_.operator} - Please use 'eq', 'ne', 'in'.",
                )
        query = query.where(and_(*conditions))

    if params.sort_by:
        sort_column = table.c[params.sort_by]
        sort_func = asc if params.sort_order == "asc" else desc
        query = query.order_by(sort_func(sort_column))

    results = db.execute(query).fetchall()

    column_names = [col.name for col in selected_columns]
    return [dict(zip(column_names, row)) for row in results]
