from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, Query

import app.routes.utils as routes_utils  # absolute import for tests
from app.dependencies import get_currency_repository
from app.models.models import Currency
from app.repository.currency_repository import CurrencyRepository
from app.schemas import schemas
from app.middleware.context_utils import get_request_id

_log = logging.getLogger(__name__)

router = APIRouter(tags=["Currencies"])


@router.post(
    "/currencies",
    status_code=201,
    summary="Fetch currencies for specified date.",
    responses={
        201: {"description": "Currency rates saved successfully."},
        400: {"description": "Currencies for the specified date already exist."},
        502: {"description": "Error fetching data from the CBR."},
        500: {"description": "Internal service error."},
    },
)
async def create_currency_rates(
    currency: schemas.CurrencyCreate,
    repo: CurrencyRepository = Depends(get_currency_repository),
) -> dict[str, str]:
    """Get currency rate for specified date from CB RF and store it in db."""
    request_date = datetime.strptime(currency.date, "%Y-%m-%d").date()
    if await repo.exists_for_date(request_date):
        raise HTTPException(
            status_code=400, detail="Data for the specified date already exists"
        )
    try:
        _log.info(f"[{get_request_id()}] Fetching data from CBR...")
        response_text = await routes_utils.fetch_currency_rates(
            request_date.strftime("%d/%m/%Y")
        )
        currency_list_json = routes_utils.parse_cbr_xml(response_text)
    except Exception as err:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching data from the CBR. {str(err)}",
        )
    try:
        currency_list = [
            Currency(code=entry["code"], rate=entry["rate"], date=request_date)
            for entry in currency_list_json
        ]
        await repo.add_multiple(currency_list)
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving data to the database. {str(err)}",
        )
    return {"message": "Currency rates saved successfully"}


@router.get(
    "/unique-currency-codes",
    response_model=list[str],
    summary="Get unique currency codes.",
    responses={
        200: {
            "description": "A list of unique currency codes",
            "content": {"application/json": {"example": ["USD", "EUR", "GBP"]}},
        },
        500: {"description": "Internal server error"},
    },
)
async def get_unique_currency_codes(
    repo: CurrencyRepository = Depends(get_currency_repository),
):
    """Get a list of unique 3-letter uppercase currency codes stored in the database."""
    return await repo.get_codes()


@router.delete(
    "/delete-by-code/{currency_code}",
    status_code=204,
    summary="Delete records by currency code.",
    responses={
        204: {"description": "Records successfully deleted"},
        400: {"description": "Invalid currency code format"},
        404: {"description": "Currency code not found"},
    },
)
async def delete_currency_by_code(
    currency_code: str, repo: CurrencyRepository = Depends(get_currency_repository)
) -> None:
    """Deletes all records in the database for the specified 3-letter
    uppercase currency code."""
    if len(currency_code) != 3 or not all(
        [c.isalpha() and c.isupper() for c in currency_code]
    ):
        raise HTTPException(status_code=400, detail="Invalid currency code format")

    deleted_count = await repo.delete_by_code(currency_code)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Currency code not found")


@router.get(
    "/all-data",
    response_model=schemas.PaginatedResponse,
    summary="Retrieve all currency data with pagination.",
    responses={
        200: {"description": "A paginated list of currency records"},
        422: {"description": "Invalid pagination parameters"},
    },
)
async def get_all_data(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Number of items per page"),
    repo: CurrencyRepository = Depends(get_currency_repository),
):
    """This endpoint retrieves a paginated list of all currency records from the
    database. The results are ordered by date in ascending order."""
    total = await repo.get_total_count()
    items = await repo.get_paginated(page, per_page)
    return {"page": page, "per_page": per_page, "total": total, "items": items}
