from dataclasses import dataclass
from typing import List
from core.models import InputData
from core.scenarios import generate_scenarios
from core.calculations import (
    potencia_hidraulica_kw,
    potencia_eletrica_estimativa_kw,
    eficiencia_global,
)

@dataclass
class CheckResult:
    codigo: str
    descricao: str
    esperado: str
    obtido: str
    aprovado: bool

def run_validation_suite() -> List[CheckResult]:
    data = InputData(
        'Validação', 'Ilhéus/BA', 'Café arábica', 'Gotejamento',
        5, 5.5, 6, 20, 0.95, 30, 10, 12, 65, 85, True, True,
        meses_operacao_ano=12
    )
    s = generate_scenarios(data)
    atual, horario, reducao, bomba, combinado = s

    data_6m = InputData(
        'Validação', 'Ilhéus/BA', 'Café arábica', 'Gotejamento',
        5, 5.5, 6, 20, 0.95, 30, 10, 12, 65, 85, True, True,
        meses_operacao_ano=6
    )
    atual_6m = generate_scenarios(data_6m)[0]

    ph = potencia_hidraulica_kw(36, 10)
    pe = potencia_eletrica_estimativa_kw(36, 10, 70, 90)
    eta = eficiencia_global(70, 90)

    checks = [
        CheckResult('V01','Consumo diário','33,00 kWh',f'{atual.consumo_diario_kwh:.2f} kWh',abs(atual.consumo_diario_kwh-33)<1e-9),
        CheckResult('V02','Consumo mensal','660,00 kWh',f'{atual.consumo_mensal_kwh:.2f} kWh',abs(atual.consumo_mensal_kwh-660)<1e-9),
        CheckResult('V03','Consumo anual em 12 meses','7.920,00 kWh',f'{atual.consumo_anual_kwh:.2f} kWh',abs(atual.consumo_anual_kwh-7920)<1e-9),
        CheckResult('V04','Custo anual','R$ 7.524,00',f'R$ {atual.custo_anual_rs:.2f}',abs(atual.custo_anual_rs-7524)<1e-9),
        CheckResult('V05','Tarifa efetiva com desconto de 30%','R$ 0,665/kWh',f'R$ {horario.tarifa_efetiva:.3f}/kWh',abs(horario.tarifa_efetiva-0.665)<1e-9),
        CheckResult('V06','Desconto tarifário não altera consumo','7.920,00 kWh',f'{horario.consumo_anual_kwh:.2f} kWh',abs(horario.consumo_anual_kwh-atual.consumo_anual_kwh)<1e-9),
        CheckResult('V07','Redução do tempo reduz consumo','menor que atual',f'{reducao.consumo_anual_kwh:.2f}',reducao.consumo_anual_kwh<atual.consumo_anual_kwh),
        CheckResult('V08','Redução simulada de potência reduz consumo','menor que atual',f'{bomba.consumo_anual_kwh:.2f}',bomba.consumo_anual_kwh<atual.consumo_anual_kwh),
        CheckResult('V09','Cenário combinado tem menor custo','menor entre cenários',f'R$ {combinado.custo_anual_rs:.2f}',combinado.custo_anual_rs==min(x.custo_anual_rs for x in s)),
        CheckResult('V10','Indicador por hectare','1.584,00 kWh/ha.ano',f'{atual.consumo_ha_kwh_ano:.2f}',abs(atual.consumo_ha_kwh_ano-1584)<1e-9),
        CheckResult('V11','Anualização sazonal em 6 meses','3.960,00 kWh',f'{atual_6m.consumo_anual_kwh:.2f}',abs(atual_6m.consumo_anual_kwh-3960)<1e-9),
        CheckResult('V12','Potência hidráulica Q=36 m³/h, H=10 m','0,981 kW',f'{ph:.3f} kW',abs(ph-0.981)<1e-9),
        CheckResult('V13','Eficiência global 70% × 90%','63,0%',f'{eta*100:.1f}%',abs(eta-0.63)<1e-9),
        CheckResult('V14','Potência elétrica estimada','1,557 kW',f'{pe:.3f} kW',abs(pe-(0.981/0.63))<1e-9),
        CheckResult('V15','Horas anuais de operação','1.440 h',f'{atual.horas_operacao_ano:.0f} h',abs(atual.horas_operacao_ano-1440)<1e-9),
    ]
    return checks
