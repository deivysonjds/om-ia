from pydantic import BaseModel, Field


class CarroResponse(BaseModel):
    id: str
    model: str
    modelYear: int
    price: float
    url_images: list[str]
    description: str
    mileage: int
    mark: str


class PerguntaRequest(BaseModel):
    pergunta: str = Field(
        ...,
        min_length=3,
        max_length=1000,
    )


class PerguntaResponse(BaseModel):
    resposta: str
    intencao: str
    estrategia: str