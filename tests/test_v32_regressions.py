import csv,re
from dataclasses import replace
from pathlib import Path
import pytest
from core.models import InputData
from core.calculations import calculate_scenario,payback_simples_meses,potencia_hidraulica_kw,eficiencia_global
from core.validation import validate_inputs
from core.scenarios import generate_scenarios
from core.indicators import classify_reliability
from core.recommendations import generate_recommendations
from core.diagnosis import generate_diagnosis
ROOT=Path(__file__).resolve().parents[1]
def sample(**kw):
 return replace(InputData('Sintético','Não se aplica','Café arábica','Gotejamento',5,5.5,6,20,.95,30,vazao_m3h=36,altura_mca=10,horas_elegiveis_desconto=6,origem_dados='Caso sintético'),**kw)

@pytest.mark.parametrize('field',['area_ha','potencia_kw','horas_dia','tarifa','vazao_m3h','altura_mca','desconto','dias_mes','meses_operacao_ano','rendimento_bomba','rendimento_motor','horas_elegiveis_desconto'])
@pytest.mark.parametrize('invalid',[float('nan'),float('inf'),float('-inf')])
def test_reject_nonfinite(field,invalid):
 d=sample(**{field:invalid});assert validate_inputs(d)
 with pytest.raises(ValueError): generate_scenarios(d)

@pytest.mark.parametrize('field',['dias_mes','meses_operacao_ano'])
def test_reject_fractional_calendar(field):
 assert validate_inputs(sample(**{field:2.5}))

def test_calendar_372_rejected():
 assert any('365' in x for x in validate_inputs(sample(dias_mes=31)))

def test_impossible_base_rejected():
 assert any('100%' in x for x in validate_inputs(sample(potencia_kw=.1,altura_mca=100)))

def test_impossible_reduction_rejected():
 assert any('redução' in x for x in validate_inputs(sample(potencia_kw=1.1,melhoria_bomba_pct=40)))

def test_360_days_accepted():
 assert not validate_inputs(sample(dias_mes=30))

def test_partial_discount_independent_reference():
 # 14,400 kWh: 10,200 at 0.7 + 4,200 at 1 = R$ 11,340.
 d=sample(potencia_kw=10,horas_dia=12,tarifa=1,meses_operacao_ano=6,horas_elegiveis_desconto=8.5)
 a,b,*_=generate_scenarios(d)
 assert a.consumo_anual_kwh==14400
 assert b.custo_anual_rs==pytest.approx(11340)
 assert b.energia_com_desconto_kwh_ano==10200
 assert b.energia_sem_desconto_kwh_ano==4200
 assert b.consumo_anual_kwh==a.consumo_anual_kwh

def test_zero_eligible_hours():
 a,b,*_=generate_scenarios(sample(horas_elegiveis_desconto=0));assert b.custo_anual_rs==a.custo_anual_rs

def test_discount_hours_capped_by_runtime():
 s=generate_scenarios(sample(horas_elegiveis_desconto=8.5))[1]
 assert s.energia_com_desconto_kwh_ano==7920 and s.energia_sem_desconto_kwh_ano==0

def test_time_reduction_preserves_specific_energy():
 a,_,b,*_=generate_scenarios(sample())
 assert b.volume_anual_m3==46656 and b.consumo_anual_kwh==7128
 assert b.consumo_especifico_kwh_1000m3==pytest.approx(a.consumo_especifico_kwh_1000m3)

def test_no_reliability_score_from_changed_default():
 assert classify_reliability(sample())==classify_reliability(sample(rendimento_bomba=66))=='Caso sintético'

@pytest.mark.parametrize('investment,economy,expected',[(0,100,0),(1200,1200,12),(500,0,None),(500,-10,None)])
def test_payback_boundaries(investment,economy,expected):
 assert payback_simples_meses(investment,economy)==expected

def test_negative_saving_preserved():
 s=calculate_scenario('Mais caro',1,1,1,1,1,custo_atual=10)
 assert s.custo_anual_rs==12 and s.economia_anual_rs==-2 and s.economia_percentual==-20

@pytest.mark.parametrize('rb,rm',[(0,90),(101,90),(70,float('nan'))])
def test_efficiency_domain(rb,rm):
 with pytest.raises(ValueError): eficiencia_global(rb,rm)

def test_core_direct_input_validation():
 with pytest.raises(ValueError): calculate_scenario('Inválido',-1,1,1,1,1)
 with pytest.raises(ValueError): calculate_scenario('Inválido',1,1,31,1,1)
 with pytest.raises(ValueError): potencia_hidraulica_kw(36,float('inf'))
 with pytest.raises(ValueError): calculate_scenario('Subnormal',1e-300,1e-300,1,1,1)
 with pytest.raises(ValueError): eficiencia_global(1e-300,1e-300)

def test_reference_integrity_in_code_and_bcci():
 rows=list(csv.DictReader((ROOT/'database/BCCI/BCCI_07_referencias.csv').open()));ids={r['id'] for r in rows}
 assert len(rows)==len(ids)
 for p in [*ROOT.glob('core/*.py'),*ROOT.glob('database/BCCI/*.csv')]:
  assert set(re.findall(r'REF\d{3}',p.read_text()))<=ids,p
 d=sample();rules=list(csv.DictReader((ROOT/'database/BCCI/BCCI_06_regras_diagnostico.csv').open()))
 assert {r['id']:r['refs'] for r in rules}=={r.codigo:r.referencias for r in generate_recommendations(d,generate_scenarios(d))}

def test_csv_reference_cases():
 for r in csv.DictReader((ROOT/'database/validacao/casos_validacao.csv').open()):
  d=sample(**{k:float(r[k]) for k in ['potencia_kw','horas_dia','dias_mes','tarifa','area_ha','desconto']},reducao_horas_pct=float(r['reducao_pct']),melhoria_bomba_pct=float(r['melhoria_pct']),vazao_m3h=None,altura_mca=None)
  s=next(s for s in generate_scenarios(d) if s.cenario==r['cenario_alvo'])
  assert s.consumo_anual_kwh==pytest.approx(float(r['consumo_esperado_kwh_ano']))
  assert s.custo_anual_rs==pytest.approx(float(r['custo_esperado_rs_ano']))

def test_report_export_and_injection_protection(tmp_path):
 from core.report import generate_excel_report,generate_pdf_report,generate_text_report
 from openpyxl import load_workbook
 from pypdf import PdfReader
 d=sample(propriedade='=HYPERLINK("https://example.invalid") <teste & revisão>');sc=generate_scenarios(d);diag=generate_diagnosis(d,sc)
 wb=load_workbook(generate_excel_report(d,sc,diag))
 assert wb['Entradas']['B2'].data_type!='f' and wb['Entradas']['B2'].value.startswith("'")
 assert set(wb.sheetnames)=={'Cenários','Entradas','Indicadores','Limitações','Orientações','Referências','Metadados'}
 pdf=generate_pdf_report(d,sc,diag,tmp_path)
 text='\n'.join(p.extract_text() for p in PdfReader(pdf).pages)
 assert '7920.00' in text and '152.78' in text and 'REF019' in text
 assert 'Caso sintético' in generate_text_report(d,sc,diag)

def test_persistence_round_trip(tmp_path,monkeypatch):
 from core import database as db
 monkeypatch.setattr(db,'DB_PATH',tmp_path/'test.db')
 d=sample();sc=generate_scenarios(d);diag=generate_diagnosis(d,sc);ident=db.save_analysis(d,sc,diag)
 assert db.get_analysis(ident)['entradas']==d.to_dict()
 assert db.get_analysis(ident)['cenarios'][0]['volume_anual_m3']==51840
 assert db.list_analyses()[0][0]==ident and db.get_analysis(ident+1) is None

def test_published_gomes_example_6_1():
 # Gomes (2013), Ex. 6.1, p. 163-166: Q=48 L/s, H=64.94 m,
 # eta_b=60%, eta_m=90%; printed Ph=30.58 kW and Pe=56.628 kW.
 # Tolerances reflect the last displayed decimal place, not field accuracy.
 from core.calculations import potencia_eletrica_estimativa_kw
 assert abs(potencia_hidraulica_kw(172.8,64.94)-30.58)<=.005
 assert abs(potencia_eletrica_estimativa_kw(172.8,64.94,60,90)-56.628)<=.0005
