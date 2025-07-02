from dataclasses import dataclass


@dataclass
class Investimento:
    ### classe para armazenar os dados do investimento
    nome: str
    valor_inicial: float
    taxa: float
    prazo: int
    cdi: float
    tipo: str  # "pre" ou "pos"


@dataclass
class ResultadoInvestimento:
    ### classe para armazenar os resultados do investimento
    nome: str
    valor_final: float
    rendimento_bruto: float
    rendimento_liquido: float
    ir_pago: float
