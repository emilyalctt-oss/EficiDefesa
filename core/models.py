from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class InputData:
    propriedade: str
    municipio: str
    cultura: str
    sistema: str
    area_ha: float
    potencia_kw: float
    horas_dia: float
    dias_mes: int
    tarifa: float
    desconto: float = 0.0
    reducao_horas_pct: float = 10.0
    melhoria_bomba_pct: float = 12.0
    rendimento_bomba: float = 65.0
    rendimento_motor: float = 85.0
    manutencao_irrigacao: bool = True
    dados_regionais: bool = True
    meses_operacao_ano: int = 12
    vazao_m3h: Optional[float] = None
    altura_mca: Optional[float] = None

    horas_elegiveis_desconto: float = 8.5
    origem_dados: str = "Não documentada"
    observacoes_dados: str = ""

    def to_dict(self):
        values = asdict(self)
        values.pop("manutencao_irrigacao", None)
        values.pop("dados_regionais", None)
        return values

@dataclass
class ScenarioResult:
    cenario: str
    potencia_kw: float
    horas_dia: float
    dias_mes: int
    tarifa_efetiva: float
    consumo_diario_kwh: float
    consumo_mensal_kwh: float
    consumo_anual_kwh: float
    custo_mensal_rs: float
    custo_anual_rs: float
    consumo_ha_kwh_ano: float
    custo_ha_rs_ano: float
    potencia_ha_kw: float
    economia_anual_rs: float = 0.0
    economia_percentual: float = 0.0
    meses_operacao_ano: int = 12
    horas_operacao_ano: float = 0.0
    volume_anual_m3: Optional[float] = None
    consumo_especifico_kwh_1000m3: Optional[float] = None
    energia_com_desconto_kwh_ano: float = 0.0
    energia_sem_desconto_kwh_ano: float = 0.0

    def to_dict(self):
        return asdict(self)
