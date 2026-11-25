"""Modelo estacionário simplificado; grandezas de entrada em unidades explícitas."""
from math import isfinite
from numbers import Real
from typing import Optional
from core.models import ScenarioResult

RHO_AGUA_KG_M3 = 1000.0
G_MS2 = 9.81

def _is_finite(value):
    try:
        return isfinite(value)
    except (OverflowError, TypeError):
        return False

def finite_number(value, name, minimum=0, maximum=None, strict=False):
    if isinstance(value, bool) or not isinstance(value, Real) or not _is_finite(value):
        raise ValueError(f"{name}: informe um número finito.")
    if value < minimum or (strict and value == minimum) or (maximum is not None and value > maximum):
        raise ValueError(f"{name}: valor fora do domínio permitido.")
    return float(value)

def integer_number(value, name, minimum, maximum):
    finite_number(value, name, minimum, maximum)
    if int(value) != value:
        raise ValueError(f"{name}: informe um inteiro.")
    return int(value)

def potencia_hidraulica_kw(vazao_m3h: float, altura_mca: float) -> float:
    """Ph[kW] = rho[kg/m³] g[m/s²] (Q[m³/h]/3600) H[m] / 1000."""
    finite_number(vazao_m3h, 'Vazão')
    finite_number(altura_mca, 'HMT')
    result = RHO_AGUA_KG_M3 * G_MS2 * (vazao_m3h / 3600) * altura_mca / 1000
    finite_number(result, 'Potência hidráulica calculada')
    return result

def eficiencia_global(rendimento_bomba: float, rendimento_motor: float) -> float:
    """Produto dos rendimentos informados; não é medição do rendimento real."""
    finite_number(rendimento_bomba, 'Rendimento da bomba', 0, 100, True)
    finite_number(rendimento_motor, 'Rendimento do motor', 0, 100, True)
    result = rendimento_bomba * rendimento_motor / 10000
    finite_number(result, "Rendimento global calculado", strict=True)
    return result

def potencia_eletrica_estimativa_kw(vazao_m3h, altura_mca, rendimento_bomba, rendimento_motor):
    result = potencia_hidraulica_kw(vazao_m3h, altura_mca) / eficiencia_global(rendimento_bomba, rendimento_motor)
    finite_number(result, 'Potência elétrica estimada')
    return result

def tarifa_efetiva(tarifa, desconto_pct=0):
    finite_number(tarifa, 'Tarifa')
    finite_number(desconto_pct, 'Desconto', 0, 100)
    return tarifa * (1 - desconto_pct / 100)

def payback_simples_meses(investimento, economia_anual):
    finite_number(investimento, 'Investimento')
    if isinstance(economia_anual, bool) or not isinstance(economia_anual, Real) or not _is_finite(economia_anual):
        raise ValueError('Economia anual deve ser finita.')
    if economia_anual <= 0:
        return None
    result = investimento / economia_anual * 12
    finite_number(result, 'Payback')
    return result

def calculate_scenario(nome: str, potencia_kw: float, horas_dia: float,
                       dias_mes: int, tarifa: float, area_ha: float,
                       desconto_pct: float = 0, custo_atual: Optional[float] = None,
                       meses_operacao_ano: int = 12, vazao_m3h: Optional[float] = None,
                       horas_elegiveis_desconto: float = 8.5) -> ScenarioResult:
    finite_number(potencia_kw, 'Potência elétrica', strict=True)
    finite_number(horas_dia, 'Horas/dia', 0, 24, True)
    finite_number(area_ha, 'Área', strict=True)
    finite_number(tarifa, 'Tarifa', strict=True)
    dias_mes = integer_number(dias_mes, 'Dias/mês', 1, 31)
    meses_operacao_ano = integer_number(meses_operacao_ano, 'Meses/ano', 1, 12)
    if dias_mes * meses_operacao_ano > 365:
        raise ValueError('O calendário simplificado não pode exceder 365 dias/ano.')
    finite_number(horas_elegiveis_desconto, 'Horas elegíveis', 0, 8.5)
    finite_number(desconto_pct, 'Desconto do cenário', 0, 90)
    td = tarifa_efetiva(tarifa, desconto_pct)
    if custo_atual is not None:
        finite_number(custo_atual, 'Custo de referência')
    hd = min(horas_dia, horas_elegiveis_desconto) if desconto_pct else 0
    horas_ano = horas_dia * dias_mes * meses_operacao_ano
    ea = potencia_kw * horas_ano
    finite_number(ea, "Energia anual calculada", strict=True)
    edesc = min(ea, potencia_kw * (hd * dias_mes * meses_operacao_ano))
    enormal = ea - edesc
    ca = edesc * td + enormal * tarifa
    finite_number(ca, "Custo anual calculado", strict=True)
    te = ca / ea
    eco = custo_atual - ca if custo_atual is not None else 0.0
    volume = especifico = None
    if vazao_m3h is not None:
        finite_number(vazao_m3h, 'Vazão', strict=True)
        volume = vazao_m3h * horas_ano
        finite_number(volume, "Volume anual calculado", strict=True)
        especifico = ea / volume * 1000
    result = ScenarioResult(
        cenario=nome, potencia_kw=potencia_kw, horas_dia=horas_dia, dias_mes=dias_mes,
        tarifa_efetiva=te, consumo_diario_kwh=potencia_kw*horas_dia,
        consumo_mensal_kwh=ea/meses_operacao_ano, consumo_anual_kwh=ea,
        custo_mensal_rs=ca/meses_operacao_ano, custo_anual_rs=ca,
        consumo_ha_kwh_ano=ea/area_ha, custo_ha_rs_ano=ca/area_ha,
        potencia_ha_kw=potencia_kw/area_ha, economia_anual_rs=eco,
        economia_percentual=eco/custo_atual*100 if custo_atual else 0,
        meses_operacao_ano=meses_operacao_ano, horas_operacao_ano=horas_ano,
        volume_anual_m3=volume, consumo_especifico_kwh_1000m3=especifico,
        energia_com_desconto_kwh_ano=edesc, energia_sem_desconto_kwh_ano=enormal)
    if any(isinstance(v, Real) and not isfinite(v) for v in result.to_dict().values()):
        raise ValueError('Resultado não finito; revise a escala dos dados.')
    return result
