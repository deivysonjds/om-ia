from models.schemas import CarroResponse

def filtrar_carros(
    carros: list[CarroResponse],
    orcamento: float | None = None,
):
    resultado = carros

    if orcamento:
        resultado = [
            carro
            for carro in resultado
            if carro.price <= orcamento
        ]

    resultado.sort(key=lambda x: x.price)

    return resultado[:10]