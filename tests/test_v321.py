from dataclasses import replace
import pytest
from core.models import InputData
from core.calculations import finite_number, calculate_scenario
from core.validation import input_warnings
from core.report import _safe_cell

def test_huge_integer():
    with pytest.raises(ValueError): finite_number(10**1000,'entrada')

def test_cost_underflow():
    with pytest.raises(ValueError): calculate_scenario('x',1e-200,1,1,1e-200,1)

def test_discount_energy_never_exceeds_total():
    s=calculate_scenario('x',0.123456789,5.123456789,29,.95,1,30,meses_operacao_ano=11)
    assert s.energia_sem_desconto_kwh_ano >= 0
    assert s.energia_com_desconto_kwh_ano <= s.consumo_anual_kwh

def test_rendimento_warning():
    d=InputData('x','x','Café arábica','Gotejamento',5,5.5,6,20,.95,vazao_m3h=36,altura_mca=10)
    assert any('difere' in w for w in input_warnings(d))

@pytest.mark.parametrize('value',[' =1+1','\t=1+1','\n@SUM(1)','+1'])
def test_formula_whitespace(value):
    assert _safe_cell(value).startswith("'")
