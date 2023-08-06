import requests

from .rates import Rates

url = "https://api.exchangeratesapi.io/latest"


def get_exchange_rates():
    r = requests.get(url)
    r.raise_for_status()

    return Rates(r.json())
