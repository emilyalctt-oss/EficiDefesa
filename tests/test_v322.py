from dataclasses import replace
import pytest
from core.models import InputData
from core.validation import validate_inputs
from core.calculations import calculate_scenario, payback_simples_meses
from core.scenarios import generate_scenarios
from core.diagnosis import generate_diagnosis
from core.report import generate_excel_report
from openpyxl import load_workbook

D = InputData('Caso sintético','Não se aplica','Café arábica','Gotejamento',5,5.5,6,20,.95,30,vazao_m3h=36,altura_mca=10)
@pytest.mark.parametrize('changes',[{'municipio':None},{'cultura':[]},{'observacoes_dados':'a'*4001},{'propriedade':'a\x00b'},{'rendimento_bomba':1e-300,'rendimento_motor':1e-300},{'vazao_m3h':1e-300,'altura_mca':1e-300}])
def test_invalid_inputs(changes):
    assert validate_inputs(replace(D,**changes))

def test_huge_savings():
    with pytest.raises(ValueError): payback_simples_meses(1,10**1000)

def test_scenario_discount_domain():
    with pytest.raises(ValueError): calculate_scenario('x',1,1,1,1,1,91)

def test_missing_investment_not_zero():
    sc=generate_scenarios(D)
    wb=load_workbook(generate_excel_report(D,sc,generate_diagnosis(D,sc)))
    assert wb['Metadados']['B2'].value=='3.2.2'
    headers=[c.value for c in wb['Cenários'][1]]
    assert wb['Cenários'].cell(2,headers.index('Investimento (R$)')+1).value is None
