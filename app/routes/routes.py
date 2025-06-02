from datetime import datetime

from fastapi import Depends, Query, APIRouter
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.dependencies import get_db
from routes.utils import fetch_currency_rates, parse_cbr_xml
from models.database import Currency
from schemas import schemas

router = APIRouter()


@router.post(
    "/currencies",
    status_code=201,
    description="Get currency rate for specified date and store it in db. ",
)
async def create_currency_rates(
    currency: schemas.CurrencyCreate, db: Session = Depends(get_db)
):
    # todo handle internal server error

    request_date = datetime.strptime(currency.date, "%Y-%m-%d").date()
    exists = db.query(Currency).filter(Currency.date == request_date).first()
    if exists:
        raise HTTPException(
            status_code=400, detail="Data for the specified dates already exists"
        )

    try:
        response_text = await fetch_currency_rates(currency.date)
        currency_list = parse_cbr_xml(response_text)
    except HTTPException:
        raise HTTPException(status_code=502, detail="Error fetching data from the CBR")

    for entry in currency_list:
        currency = Currency(code=entry["code"], rate=entry["rate"], date=request_date)
        db.add(currency)
    db.commit()
    return {"message": "Currency rates saved successfully"}


@router.get("/unique-currency-codes", response_model=list[str])
def get_unique_currency_codes(db: Session = Depends(get_db)):
    codes = db.query(Currency.code).distinct().all()
    return sorted([code[0] for code in codes])


@router.delete("/delete-by-code/{currency_code}")
def delete_currency_by_code(currency_code: str, db: Session = Depends(get_db)):
    if len(currency_code) != 3 or not all(
        [c.isalpha() and c.isupper() for c in currency_code]
    ):
        raise HTTPException(status_code=400, detail="Invalid currency code format")

    deleted_count = db.query(Currency).filter(Currency.code == currency_code).delete()
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Currency code not found")

    db.commit()
    return {"message": f"All records for {currency_code} deleted successfully"}


@router.get("/all-data", response_model=schemas.PaginatedResponse)
def get_all_data(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Currency).count()
    items = db.query(Currency).offset((page - 1) * per_page).limit(per_page).all()
    return {"page": page, "per_page": per_page, "total": total, "items": items}
