import re
import httpx
import respx
from httpx import Response


def mock_gecko_for_single_coin(coin_api_id: str, status_code: int):
    data = {
        "id": coin_api_id,
        "symbol": "btc",
        "name": "Bitcoin",
        'description': {'en': 'descr'},
        "market_data": {
            "current_price": {"usd": 60000.0}
        }
    }
    route = respx.get(re.compile(fr".*coingecko\.com/api/v3/coins/{coin_api_id}.*"))
    if status_code == 500:
        route.mock(side_effect = httpx.ReadTimeout('Connection timed out.'))
    else:
        route.mock(return_value=Response(status_code=status_code, json=data))

    return route


def mock_gecko_for_multiple_coins():
    data = {
        "bitcoin": {
            "usd": 79265
        }
    }
    pattern = re.compile(
        fr".*api\.coingecko\.com/api/v3/simple/price\?vs_currencies=[^&]+&ids=[^&]+"
    )
    route = respx.get(pattern).mock(return_value=Response(status_code=200, json=data))
    return route
