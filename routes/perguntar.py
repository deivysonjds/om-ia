from fastapi import APIRouter
from fastapi import HTTPException

from app.models.schemas import (
    PerguntaRequest,
    PerguntaResponse
)

from app.services.agent_service import (
    executar_agente
)

import traceback

router = APIRouter()


@router.post(
    "/ask",
    response_model=PerguntaResponse
)
async def perguntar(req: PerguntaRequest):

    try:

        resultado = executar_agente(
            req.pergunta
        )

        return PerguntaResponse(
            **resultado
        )

    except Exception as e:
        print("\n========== ERRO ==========")
        traceback.print_exc()
        print("==========================\n")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )