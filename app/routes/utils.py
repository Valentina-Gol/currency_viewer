import xmltodict
from httpx import AsyncClient

from app.settings import CB_RF_URL


async def fetch_currency_rates(date: str) -> str:
    async with AsyncClient(base_url=CB_RF_URL) as client:
        response = await client.get(f"/XML_daily.asp?date_req={date}")
        return response.text


def parse_cbr_xml(xml_text: str) -> list[dict[str, str | float]]:
    xml_info = xmltodict.parse(xml_text)
    if "Valute" not in xml_info["ValCurs"]:
        raise ValueError(xml_info["ValCurs"])

    currency_data = []
    for currency_item in xml_info["ValCurs"]["Valute"]:
        code = currency_item["CharCode"]
        nominal = int(currency_item["Nominal"])
        rate_value = float(currency_item["Value"].replace(",", ".")) / nominal
        currency_data.append({"code": code, "rate": rate_value})
    return currency_data
