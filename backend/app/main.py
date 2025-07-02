from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.models import Investimento
from app.logic import calcular_cdb, calcular_lca_lci

app = FastAPI()

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio correto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvestimentoRequest(BaseModel):
    escolha: str
    tipo: str
    valor: float
    taxa: float
    prazo: int
    cdi: float


@app.post("/calcular")
def calcular_investimento(request: InvestimentoRequest):
    # Converter percentuais para decimais
    taxa = request.taxa / 100
    cdi = request.cdi / 100

    investimento = Investimento(
        request.escolha, request.valor, taxa, request.prazo, cdi, request.tipo
    )

    if request.escolha.upper() == "CDB":
        resultado = calcular_cdb(investimento)
    elif request.escolha.upper() in ["LCA", "LCI"]:
        resultado = calcular_lca_lci(investimento)
    else:
        return {"erro": "Tipo de investimento inválido"}

    ganho_nominal = resultado.valor_final - investimento.valor_inicial

    return {
        "ganho_nominal": round(ganho_nominal, 2),
        "valor_final": round(resultado.valor_final, 2),
        "ir_pago": round(resultado.ir_pago, 2),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
