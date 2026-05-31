from langgraph.graph import END
from langgraph.graph import StateGraph

from app.agent.state import AgentState

from app.agent.nodes import (
    no_entrada,
    no_classificar,
    no_recuperar,
    no_decidir,
    gerar_recomendacao,
    gerar_comparacao,
    gerar_duvida_geral,
    gerar_orcamento_insuficiente,
    gerar_alternativas
)


def route(state):

    estrategia = state["estrategia"]

    if estrategia == "comparar":
        return "comparacao"

    if estrategia == "responder_geral":
        return "duvida"

    if estrategia == "informar_orcamento":
        return "orcamento"

    if estrategia == "sugerir_alternativas":
        return "alternativas"

    return "recomendacao"


graph = StateGraph(AgentState)

graph.add_node("entrada", no_entrada)
graph.add_node("classificar", no_classificar)
graph.add_node("recuperar", no_recuperar)
graph.add_node("decidir", no_decidir)

graph.add_node(
    "gerar_recomendacao",
    gerar_recomendacao
)

graph.add_node(
    "gerar_comparacao",
    gerar_comparacao
)

graph.add_node(
    "gerar_duvida_geral",
    gerar_duvida_geral
)

graph.add_node(
    "gerar_orcamento",
    gerar_orcamento_insuficiente
)

graph.add_node(
    "gerar_alternativas",
    gerar_alternativas
)

graph.set_entry_point("entrada")

graph.add_edge(
    "entrada",
    "classificar"
)

graph.add_edge(
    "classificar",
    "recuperar"
)

graph.add_edge(
    "recuperar",
    "decidir"
)

graph.add_conditional_edges(
    "decidir",
    route,
    {
        "recomendacao": "gerar_recomendacao",
        "comparacao": "gerar_comparacao",
        "duvida": "gerar_duvida_geral",
        "orcamento": "gerar_orcamento",
        "alternativas": "gerar_alternativas",
    }
)

graph.add_edge(
    "gerar_recomendacao",
    END
)

graph.add_edge(
    "gerar_comparacao",
    END
)

graph.add_edge(
    "gerar_duvida_geral",
    END
)

graph.add_edge(
    "gerar_orcamento",
    END
)

graph.add_edge(
    "gerar_alternativas",
    END
)

agente = graph.compile()