import pytest
from core.models import InputData
from core.scenarios import generate_scenarios
from core.calculations import (
    potencia_hidraulica_kw,
    potencia_eletrica_estimativa_kw,
    eficiencia_global,
)
from core.validation import validate_inputs
from core.validation_suite import run_validation_suite

def make(**kw):
    base = dict(
        propriedade="Teste", municipio="Ilhéus/BA", cultura="Café arábica",
        sistema="Gotejamento", area_ha=5, potencia_kw=5.5, horas_dia=6,
        dias_mes=20, tarifa=0.95, desconto=30, reducao_horas_pct=10,
        melhoria_bomba_pct=12, rendimento_bomba=65, rendimento_motor=85,
        manutencao_irrigacao=True, dados_regionais=True,
        meses_operacao_ano=12, vazao_m3h=None, altura_mca=None,
    )
    base.update(kw)
    return InputData(**base)

def test_anualizacao_respeita_meses_operacao():
    a = generate_scenarios(make(meses_operacao_ano=12))[0]
    b = generate_scenarios(make(meses_operacao_ano=6))[0]
    assert b.consumo_anual_kwh == pytest.approx(a.consumo_anual_kwh / 2)
    assert b.custo_anual_rs == pytest.approx(a.custo_anual_rs / 2)

def test_desconto_tarifario_nao_reduz_energia():
    atual, horario, *_ = generate_scenarios(make())
    assert horario.consumo_anual_kwh == pytest.approx(atual.consumo_anual_kwh)
    assert horario.custo_anual_rs < atual.custo_anual_rs

def test_hidraulica_opcional():
    data = make(vazao_m3h=36, altura_mca=10)
    atual = generate_scenarios(data)[0]
    assert atual.volume_anual_m3 == pytest.approx(36 * 6 * 20 * 12)
    assert atual.consumo_especifico_kwh_1000m3 is not None

def test_potencia_hidraulica_e_eletrica():
    ph = potencia_hidraulica_kw(36, 10)
    assert ph == pytest.approx(0.981)
    assert eficiencia_global(70, 90) == pytest.approx(0.63)
    assert potencia_eletrica_estimativa_kw(36, 10, 70, 90) == pytest.approx(0.981 / 0.63)

def test_vazao_e_hmt_devem_ser_informadas_juntas():
    errors = validate_inputs(make(vazao_m3h=20, altura_mca=None))
    assert any("vazão e altura manométrica" in e.lower() for e in errors)

def test_suite_interna_v31():
    checks = run_validation_suite()
    assert len(checks) >= 15
    assert all(c.aprovado for c in checks)
