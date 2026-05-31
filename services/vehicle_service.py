import requests

from app.models.schemas import CarroResponse
from app.config import URL_API


def buscar_veiculos() -> list[CarroResponse]:

    response = requests.get(
        f"{URL_API}/vehicles/",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return [
        CarroResponse(**item)
        for item in data
    ]