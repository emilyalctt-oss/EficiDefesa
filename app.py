from pathlib import Path
import json,tempfile,os
import pandas as pd
import streamlit as st
from core.models import InputData
from core.validation import validate_inputs
from core.scenarios import generate_scenarios
from core.diagnosis import generate_diagnosis
from core.calculations import payback_simples_meses
from core.report import scenarios_dataframe,technical_values,generate_excel_report,generate_pdf_report,generate_text_report
from core.database import save_analysis,list_analyses,get_analysis
from core.validation_suite import run_validation_suite

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='EficiAgro V3.2.2',page_icon=str(ROOT/'assets/favicon.png'),layout='wide')
st.logo(str(ROOT/'assets/logo_horizontal.png'))
st.title('EficiAgro')
st.caption('V3.2.2 · Análise energética e comparação de custos na irrigação da cafeicultura')
st.info('Protótipo computacional sem validação em campo. Simulação de apoio à decisão. O menor custo calculado não comprova viabilidade técnica, atendimento hídrico ou economia real.')
with st.sidebar:
    st.image(str(ROOT/'assets/logo_horizontal.png'),width=240)
    st.header('Dados da análise')
    with st.expander('Propriedade e origem dos dados',expanded=True):
        prop=st.text_input('Propriedade','Caso sintético demonstrativo',max_chars=200)
        mun=st.text_input('Município/UF','Não se aplica — caso sintético',max_chars=200)
        cultura=st.selectbox('Cultura',['Café arábica','Café conilon'])
        sistema=st.selectbox('Sistema',['Gotejamento','Microaspersão'])
        area=st.number_input('Área irrigada (ha)',min_value=.01,value=5.0)
        origem=st.selectbox('Origem declarada dos dados',['Caso sintético','Estimativas do usuário','Medições/documentos declarados','Não documentada'])
        obs=st.text_area('Origem, data, instrumento ou documento','Exemplo para verificação numérica; não representa uma propriedade real.',max_chars=4000)
        st.caption('A declaração não é verificada pelo programa e não gera nota de confiabilidade.')
    with st.expander('Operação energética',expanded=True):
        pot=st.number_input('Potência elétrica ativa de entrada (kW)',min_value=.001,value=5.5)
        st.caption('Use potência elétrica representativa da operação. Potência nominal no eixo do motor não é equivalente.')
        horas=st.number_input('Horas de operação por dia',min_value=.01,max_value=24.0,value=6.0)
        dias=st.number_input('Dias de operação por mês',min_value=1,max_value=31,value=20)
        meses=st.number_input('Meses de operação por ano',min_value=1,max_value=12,value=12)
        tarifa=st.number_input('Tarifa base de energia ativa (R$/kWh)',min_value=.001,value=.95,format='%.3f')
        st.caption('A tarifa base representa a condição atual. O modelo não calcula demanda, tributos ou encargos separadamente.')
    with st.expander('Dados hidráulicos'):
        hid=st.checkbox('Informar vazão e HMT',value=True)
        q=st.number_input('Vazão (m³/h)',min_value=.001,value=36.0) if hid else None
        h=st.number_input('Altura manométrica total (m)',min_value=.001,value=10.0) if hid else None
        rb=st.number_input('Rendimento informado da bomba (%)',min_value=.1,max_value=100.0,value=65.0)
        rm=st.number_input('Rendimento informado do motor (%)',min_value=.1,max_value=100.0,value=85.0)
        st.caption('Vazão, HMT e potência devem corresponder ao mesmo ponto de operação. Os rendimentos não substituem a potência elétrica informada nos cenários.')
    with st.expander('Hipóteses dos cenários',expanded=True):
        desconto=st.slider('Desconto hipotético nas horas elegíveis (%)',0,90,30)
        elegiveis=st.number_input('Horas elegíveis por dia no cenário tarifário',min_value=0.0,max_value=8.5,value=6.0,step=.5)
        st.caption('No caso sintético, são 6 h elegíveis. Para dados reais, confirme enquadramento e escala com a distribuidora. Não há identificação automática do benefício.')
        reducao=st.slider('Redução hipotética do tempo (%)',0,50,10)
        melhoria=st.slider('Redução hipotética da potência (%)',0,40,12)
    with st.expander('Investimentos por cenário'):
        iv1=st.number_input('Adequação tarifária (R$)',min_value=0.0,value=500.0)
        iv2=st.number_input('Ajuste do tempo (R$)',min_value=0.0,value=0.0)
        iv3=st.number_input('Intervenção na motobomba (R$)',min_value=0.0,value=8000.0)
        iv4=st.number_input('Conjunto de medidas (R$)',min_value=0.0,value=8500.0)
        st.caption('Investimentos independentes e hipotéticos. Payback simples; não é análise de viabilidade completa.')

data=InputData(prop,mun,cultura,sistema,area,pot,horas,dias,tarifa,desconto,reducao,melhoria,rb,rm,
               meses_operacao_ano=meses,vazao_m3h=q,altura_mca=h,horas_elegiveis_desconto=elegiveis,
               origem_dados=origem,observacoes_dados=obs)
errors=validate_inputs(data)
if errors:
    for err in errors: st.error(err)
    st.stop()
try:
    scenarios=generate_scenarios(data)
    diagnosis=generate_diagnosis(data,scenarios)
    technical=technical_values(data)
except ValueError as exc:
    st.error(str(exc));st.stop()
invest=dict(zip([s.cenario for s in scenarios],[0,iv1,iv2,iv3,iv4]))
try:
    paybacks={s.cenario:payback_simples_meses(invest[s.cenario],s.economia_anual_rs) for s in scenarios}
except ValueError as exc:
    st.error(str(exc)); st.stop()
diagnosis['investimentos']=invest;diagnosis['paybacks_meses']=paybacks;diagnosis['versao']='3.2.2'
base=scenarios[0]; best=min(scenarios,key=lambda s:s.custo_anual_rs)
cols=st.columns(3)
cols[0].metric('Consumo anual atual',f'{base.consumo_anual_kwh:,.2f} kWh')
cols[1].metric('Custo anual atual',f'R$ {base.custo_anual_rs:,.2f}')
cols[2].metric('Redução de custo simulada máxima',f'{best.economia_percentual:.2f}%')
st.caption('Menor custo simulado: '+best.cenario+'. A escolha considera apenas custo de energia, sem investimento ou restrições agronômicas.')
tabs=st.tabs(['Cenários','Indicadores e limites','Orientações e fontes','Verificação','Histórico e exportação'])
with tabs[0]:
    frame=scenarios_dataframe(scenarios)
    st.dataframe(frame,hide_index=True,width='stretch')
    st.bar_chart(frame.set_index('Cenário')[['Consumo anual (kWh)']])
    st.warning('Redução do tempo: menos energia e menos água. Compare também o volume e o consumo específico. A ferramenta não verifica demanda hídrica.')
    st.dataframe(pd.DataFrame({'Cenário':invest.keys(),'Investimento (R$)':invest.values(),'Payback simples (meses)':paybacks.values()}),hide_index=True)
    st.caption('Payback = 12 × investimento / economia anual. Economia não positiva: não aplicável. Investimento zero e economia positiva: zero meses. Não considera juros, inflação ou manutenção.')
with tabs[1]:
    st.dataframe(pd.DataFrame(technical.items(),columns=['Indicador','Valor']),hide_index=True)
    st.write('A potência elétrica estimada pelos rendimentos é informativa; os cenários usam a potência elétrica de entrada declarada.')
    st.write('Consumo específico: energia anual / volume anual × 1.000. Depende também da HMT; não é referência universal para sistemas distintos.')
    for msg in diagnosis['alertas']: st.write('• '+msg)
    st.write('Origem declarada: **'+data.origem_dados+'**')
    st.text(data.observacoes_dados)
with tabs[2]:
    st.dataframe(pd.DataFrame(diagnosis['recomendacoes'])[['recomendacao','justificativa','referencias']],hide_index=True)
    files=sorted((ROOT/'database/BCCI').glob('*.csv'))
    choice=st.selectbox('Base técnica consultável',[f.name for f in files])
    st.dataframe(pd.read_csv(ROOT/'database/BCCI'/choice),hide_index=True)
    st.caption('Orientações condicionais. A base documenta fontes e limites; não é um sistema especialista validado em campo.')
with tabs[3]:
    checks=run_validation_suite()
    st.write(f'{sum(c.aprovado for c in checks)} de {len(checks)} verificações internas aprovadas.')
    st.dataframe(pd.DataFrame([vars(c) for c in checks]),hide_index=True)
    st.caption('Suíte interna é parte da verificação computacional. O conjunto de regressão completo é executado com pytest. Nenhum dos testes equivale a validação agronômica ou de campo.')
with tabs[4]:
    st.download_button('Baixar relatório Excel',generate_excel_report(data,scenarios,diagnosis,invest,paybacks),file_name='EficiAgro_analise.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.download_button('Baixar relatório de texto',generate_text_report(data,scenarios,diagnosis),file_name='EficiAgro_analise.txt')
    st.download_button('Baixar dados completos JSON',json.dumps({'versao':'3.2.2','entradas':data.to_dict(),'cenarios':[s.to_dict() for s in scenarios],'diagnostico':diagnosis},ensure_ascii=False,indent=2),file_name='EficiAgro_analise.json',mime='application/json')
    payload=json.dumps({'entradas':data.to_dict(),'diagnostico':diagnosis},sort_keys=True,ensure_ascii=False)
    if st.button('Preparar relatório PDF'):
        with tempfile.TemporaryDirectory() as folder:
            pdf=generate_pdf_report(data,scenarios,diagnosis,folder,invest,paybacks)
            st.session_state['pdf_export']=(payload,Path(pdf).read_bytes())
    cached=st.session_state.get('pdf_export')
    if cached and cached[0]==payload:
        st.download_button('Baixar relatório PDF',cached[1],file_name='EficiAgro_analise.pdf',mime='application/pdf')
    st.caption('Histórico local opcional, sem autenticação. Habilite somente em instalação individual privada.')
    if os.environ.get('EFICIAGRO_ENABLE_HISTORY') == '1':
        if st.button('Salvar análise no histórico local'):
            identifier=save_analysis(data,scenarios,diagnosis);st.success(f'Análise {identifier} salva.')
        rows=list_analyses()
        if rows:
            st.dataframe(pd.DataFrame(rows,columns=['ID','Data UTC','Propriedade','Cultura','Sistema']),hide_index=True)
            ident=st.selectbox('Consultar análise salva',[r[0] for r in rows])
            st.json(get_analysis(ident),expanded=False)
        else: st.write('Nenhuma análise salva.')
    else:
        st.info('Histórico desabilitado por padrão para proteger dados em instalações compartilhadas. Use as exportações.')
