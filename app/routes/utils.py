from fastapi import HTTPException
from httpx import AsyncClient
import xmltodict


async def fetch_currency_rates(date: str):
    async with AsyncClient() as client:
        response = await client.get(
            f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
        )
        # todo status 200 but error -.-
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Error on getting data from Central Bank of Russia",
            )
        return response.text


def parse_cbr_xml(xml_text: str):
    xml_info = xmltodict.parse(xml_text)
    currency_data = []
    for currency_item in xml_info["ValCurs"]["Valute"]:
        code = currency_item["CharCode"]
        nominal = int(currency_item["Nominal"])
        rate_value = float(currency_item["Value"].replace(",", ".")) / nominal
        currency_data.append({"code": code, "rate": rate_value})
    return currency_data
