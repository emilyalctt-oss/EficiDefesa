"""Reference arithmetic uses Decimal, independently of production functions.
Run from any directory: python scripts/verify_numeric.py
"""
import csv,json,sys,platform
from decimal import Decimal as D
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
def installed(name):
 try: return version(name)
 except PackageNotFoundError: return "não instalado"
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core.models import InputData
from core.scenarios import generate_scenarios
from core.calculations import potencia_hidraulica_kw,potencia_eletrica_estimativa_kw
from core.report import scenarios_dataframe
from core.validation_suite import run_validation_suite
out=ROOT/'validation/results';out.mkdir(parents=True,exist_ok=True)
data=InputData('Caso sintético demonstrativo','Não se aplica','Café arábica','Gotejamento',5,5.5,6,20,.95,30,vazao_m3h=36,altura_mca=10,horas_elegiveis_desconto=6,origem_dados='Caso sintético',observacoes_dados='Valores didáticos; sem levantamento de campo.')
sc=generate_scenarios(data);rows=[]
def check(name,expected,obtained,tol=D('1e-8'),origin='Aritmética decimal independente'):
 error=abs(D(str(obtained))-D(str(expected)))
 rows.append(dict(indicador=name,referencia=str(expected),obtido=repr(obtained),erro_absoluto=str(error),tolerancia=str(tol),aprovado=error<=tol,origem=origin))
for s,fp,fh,desc in zip(sc,['1','1','1','.88','.88'],['1','1','.9','1','.9'],['0','.30','0','0','.30']):
 power=D('5.5')*D(fp);hours=D('6')*D(fh);days=D('20')*D('12')
 energy=power*hours*days;volume=D('36')*hours*days
 cost=energy*D('.95')*(1-D(desc)) # All hours eligible in this reference case.
 for name,expected,obtained in [('energia',energy,s.consumo_anual_kwh),('custo',cost,s.custo_anual_rs),('volume',volume,s.volume_anual_m3),('consumo_especifico',1000*energy/volume,s.consumo_especifico_kwh_1000m3)]:
  check(s.cenario+' / '+name,expected,obtained)
check('Ph sintético',D('1000')*D('9.81')*(D('36')/3600)*D('10')/1000,potencia_hidraulica_kw(36,10))
check('Pe sintético eta=0.63',D('.981')/D('.63'),potencia_eletrica_estimativa_kw(36,10,70,90))
check('Ph exemplo publicado',D('30.58'),potencia_hidraulica_kw(172.8,64.94),D('.005'),'Gomes (2013), Exemplo 6.1 conforme registro anterior; fonte primária não reconferida')
check('Pe exemplo publicado',D('56.628'),potencia_eletrica_estimativa_kw(172.8,64.94,60,90),D('.0005'),'Gomes (2013), Exemplo 6.1 conforme registro anterior; fonte primária não reconferida')
from dataclasses import replace
partial=generate_scenarios(replace(data,potencia_kw=10,horas_dia=12,tarifa=1,meses_operacao_ano=6,horas_elegiveis_desconto=8.5))[1]
check('Tarifa parcial / custo',D('10200')*D('.7')+D('4200'),partial.custo_anual_rs)
with (out/'comparacao_numerica.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
scenarios_dataframe(sc).to_csv(out/'cenarios_caso_sintetico.csv',index=False)
(out/'caso_sintetico.json').write_text(json.dumps(data.to_dict(),ensure_ascii=False,indent=2))
(out/'ambiente.json').write_text(json.dumps({'python':platform.python_version(),'plataforma':platform.platform(),'dependencias':{x:installed(x) for x in ['streamlit','pandas','openpyxl','reportlab','pytest','pypdf']}},indent=2))
internal=run_validation_suite()
(out/'suite_interna.json').write_text(json.dumps([vars(c) for c in internal],ensure_ascii=False,indent=2))
summary={'comparacoes':len(rows),'aprovadas':sum(r['aprovado'] for r in rows),'suite_interna':len(internal),'suite_aprovadas':sum(r.aprovado for r in internal),'natureza':'Verificação computacional e comparação com exemplo publicado; sem validação de campo.'}
(out/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False))
assert all(r['aprovado'] for r in rows) and all(r.aprovado for r in internal)
