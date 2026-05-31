import re

from typing import Optional

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from app.agent.state import AgentState
from app.services.vehicle_service import buscar_veiculos
from app.services.filter_service import filtrar_carros
from app.config import LLM_MODEL


def _get_llm():

    return ChatOpenAI(
        model=LLM_MODEL,
        temperature=0.5
    )


def _extrair_orcamento(texto: str) -> Optional[float]:

    texto = texto.lower()

    padroes = [
        r"([\d]+)\s*mil",
        r"([\d]+)\s*k\b",
        r"r?\$?\s*([\d\.]+)"
    ]

    for padrao in padroes:

        match = re.search(padrao, texto)

        if match:

            valor = float(
                match.group(1)
                .replace(".", "")
                .replace(",", ".")
            )

            if "mil" in padrao or "k" in padrao:
                valor *= 1000

            if valor < 1000:
                valor *= 1000

            return valor

    return None


def no_entrada(state: AgentState):

    return {
        "pergunta": state["pergunta"],
        "orcamento": _extrair_orcamento(
            state["pergunta"]
        )
    }


def no_classificar(state: AgentState):

    llm = _get_llm()

    prompt = """
Classifique a intenção.

Retorne apenas:

busca_carro
comparacao
duvida_geral
orcamento_insuficiente
"""

    response = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=state["pergunta"])
    ])

    intencao = response.content.strip()

    if (
        state.get("orcamento")
        and state["orcamento"] < 50000
    ):
        intencao = "orcamento_insuficiente"

    return {
        "intencao": intencao
    }


def no_recuperar(state: AgentState):

    carros = buscar_veiculos()

    carros = filtrar_carros(
        carros,
        state.get("orcamento")
    )

    if not carros:

        return {
            "contexto": "Nenhum veículo encontrado."
        }

    contexto = []

    for carro in carros:

        contexto.append(
            f"""
Marca: {carro.mark}
Modelo: {carro.model}
Ano: {carro.modelYear}
Preço: {carro.price}
Quilometragem: {carro.mileage}
Características: {carro.description}
"""
        )

    return {
        "contexto": "\n\n".join(contexto)
    }


def no_decidir(state: AgentState):

    intencao = state["intencao"]

    if intencao == "comparacao":
        return {"estrategia": "comparar"}

    if intencao == "duvida_geral":
        return {"estrategia": "responder_geral"}

    if intencao == "orcamento_insuficiente":
        return {"estrategia": "informar_orcamento"}

    return {"estrategia": "recomendar"}


def _gerar(system_prompt, state):

    llm = _get_llm()

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"""
Pergunta:

{state['pergunta']}

Contexto:

{state['contexto']}
"""
        )
    ])

    return {
        "resposta": response.content
    }


def gerar_recomendacao(state):

    return _gerar(
        """
Você é um consultor automotivo.

Recomende veículos usando exclusivamente o contexto informado.

Use markdown.
""",
        state
    )


def gerar_comparacao(state):

    return _gerar(
        """
Compare os veículos mencionados.

Monte tabela quando possível.
""",
        state
    )


def gerar_duvida_geral(state):

    return _gerar(
        """
Responda a dúvida do usuário.
""",
        state
    )


def gerar_orcamento_insuficiente(state):

    return _gerar(
        """
O orçamento é insuficiente.

Explique isso de forma educada.
""",
        state
    )


def gerar_alternativas(state):

    return _gerar(
        """
Sugira alternativas próximas.
""",
        state
    )