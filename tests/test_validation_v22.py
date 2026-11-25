
import csv
from pathlib import Path
import pytest
from core.models import InputData
from core.scenarios import generate_scenarios
from core.calculations import potencia_hidraulica_kw, potencia_eletrica_estimativa_kw
from core.validation_suite import run_validation_suite

ROOT=Path(__file__).resolve().parents[1]

def make(**kw):
    base=dict(propriedade='Teste',municipio='Ilhéus/BA',cultura='Café arábica',sistema='Gotejamento',area_ha=5,potencia_kw=5.5,horas_dia=6,dias_mes=20,tarifa=0.95,desconto=30,reducao_horas_pct=10,melhoria_bomba_pct=12,rendimento_bomba=65,rendimento_motor=85,manutencao_irrigacao=True,dados_regionais=True)
    base.update(kw); return InputData(**base)

def test_suite_interna_aprovada():
    assert all(c.aprovado for c in run_validation_suite())

def test_aumento_potencia_aumenta_consumo():
    a=generate_scenarios(make(potencia_kw=5))[0]
    b=generate_scenarios(make(potencia_kw=10))[0]
    assert b.consumo_anual_kwh == pytest.approx(2*a.consumo_anual_kwh)

def test_aumento_horas_aumenta_consumo():
    a=generate_scenarios(make(horas_dia=4))[0]
    b=generate_scenarios(make(horas_dia=8))[0]
    assert b.consumo_anual_kwh == pytest.approx(2*a.consumo_anual_kwh)

def test_tarifa_altera_custo_nao_consumo():
    a=generate_scenarios(make(tarifa=0.5))[0]
    b=generate_scenarios(make(tarifa=1.0))[0]
    assert b.consumo_anual_kwh == pytest.approx(a.consumo_anual_kwh)
    assert b.custo_anual_rs == pytest.approx(2*a.custo_anual_rs)

def test_area_altera_especifico_nao_total():
    a=generate_scenarios(make(area_ha=5))[0]
    b=generate_scenarios(make(area_ha=10))[0]
    assert a.consumo_anual_kwh == pytest.approx(b.consumo_anual_kwh)
    assert b.consumo_ha_kwh_ano == pytest.approx(a.consumo_ha_kwh_ano/2)

def test_potencia_hidraulica():
    assert potencia_hidraulica_kw(36,10) == pytest.approx(0.981)

def test_potencia_eletrica_estimativa():
    assert potencia_eletrica_estimativa_kw(36,10,70,90) == pytest.approx(0.981/0.63)

def test_integridade_bcci_referencias():
    ref_file=ROOT/'database'/'BCCI'/'BCCI_07_referencias.csv'
    refs={r['id'] for r in csv.DictReader(open(ref_file,encoding='utf-8'))}
    assert refs, "Base bibliográfica vazia"
    for p in (ROOT/'database'/'BCCI').glob('BCCI_*.csv'):
        if p.name=='BCCI_07_referencias.csv': continue
        rows=list(csv.DictReader(open(p,encoding='utf-8')))
        assert rows, f'{p.name} vazio'
        for row in rows:
            if 'refs' in row and row['refs']:
                for rid in row['refs'].split(';'):
                    assert rid.strip() in refs, f'{rid} ausente em {p.name}'
