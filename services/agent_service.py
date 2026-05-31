from app.agent.graph import agente


def executar_agente(pergunta: str):

    estado = {
        "pergunta": pergunta,
        "intencao": "",
        "orcamento": None,
        "contexto": "",
        "estrategia": "",
        "resposta": "",
    }

    resultado = agente.invoke(estado)

    return {
        "resposta": resultado["resposta"],
        "intencao": resultado["intencao"],
        "estrategia": resultado["estrategia"],
    }