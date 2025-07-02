from app.models import Investimento, ResultadoInvestimento
from app.utils import calcular_aliquota_ir


def calcular_cdb(investimento: Investimento) -> ResultadoInvestimento:
    if investimento.tipo == "pre":
        # Taxa anual convertida para diária
        taxa_diaria = investimento.taxa / 365
        rendimento_bruto = investimento.valor_inicial * (
            (1 + taxa_diaria) ** investimento.prazo
        )
    elif investimento.tipo == "pos":
        # Taxa anual convertida para diária
        taxa_diaria = (investimento.taxa * investimento.cdi) / 365
        rendimento_bruto = investimento.valor_inicial * (
            (1 + taxa_diaria) ** investimento.prazo
        )
    else:
        raise ValueError("Tipo de investimento inválido: Use 'pre' ou 'pos'")

    ir = (rendimento_bruto - investimento.valor_inicial) * calcular_aliquota_ir(
        investimento.prazo
    )
    rendimento_liquido = rendimento_bruto - ir
    return ResultadoInvestimento(
        nome=investimento.nome,
        valor_final=rendimento_liquido,
        rendimento_bruto=rendimento_bruto,
        rendimento_liquido=rendimento_liquido,
        ir_pago=ir,
    )


def calcular_lca_lci(investimento: Investimento) -> ResultadoInvestimento:
    if investimento.tipo == "pre":
        # Taxa anual convertida para diária
        taxa_diaria = investimento.taxa / 365
        rendimento_bruto = investimento.valor_inicial * (
            (1 + taxa_diaria) ** investimento.prazo
        )
    elif investimento.tipo == "pos":
        # Taxa anual convertida para diária
        taxa_diaria = (investimento.taxa * investimento.cdi) / 365
        rendimento_bruto = investimento.valor_inicial * (
            (1 + taxa_diaria) ** investimento.prazo
        )
    else:
        raise ValueError("Tipo de investimento inválido: Use 'pre' ou 'pos'")

    return ResultadoInvestimento(
        nome=investimento.nome,
        valor_final=rendimento_bruto,
        rendimento_bruto=rendimento_bruto,
        rendimento_liquido=rendimento_bruto,
        ir_pago=0,
    )
