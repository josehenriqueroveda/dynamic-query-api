from typing import List
from typing import Optional

from api.models.example_model import ExampleModel
from core.db import get_db
from core.security import request_limiter
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import Request
from sqlalchemy import text
from sqlalchemy.orm import Session

example_route = APIRouter(prefix="/example")
limiter = request_limiter.get_limiter()


@example_route.get("/examples", response_model=List[ExampleModel])
@limiter.limit("60/minute")
async def get_sales_forecast(
    request: Request,
    parameter_1: str = Query(..., alias="parameter1 is required"),
    parameter_2: Optional[int] = Query(default=0, alias="parameter2 is optional"),
    db: Session = Depends(get_db),
):
    """ """
    try:
        base_query = """SELECT x_date, x_mandatory_string, x_optional_string, x_optional_int, x_optional_list
                        FROM schema.table
                        WHERE x_date <= DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year' - INTERVAL '1 day'
                        """

        result = db.execute(text(base_query)).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="Examples not found")

        examples = [
            ExampleModel(
                x_date=row[0],
                x_mandatory_string=row[1],
                x_optional_string=row[2],
                x_optional_int=row[3],
                x_optional_list=row[4],
            )
            for row in result
        ]

        return examples

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
