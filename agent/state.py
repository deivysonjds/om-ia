from typing import Optional
from typing_extensions import TypedDict


class AgentState(TypedDict):

    pergunta: str

    intencao: str

    orcamento: Optional[float]

    contexto: str

    estrategia: str

    resposta: str