"""Exportação reproduzível das entradas, saídas, hipóteses e fontes."""
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape
import io
import pandas as pd
from core.calculations import eficiencia_global, potencia_hidraulica_kw, potencia_eletrica_estimativa_kw

ROOT=Path(__file__).resolve().parents[1]

INPUT_LABELS={'propriedade': 'Propriedade', 'municipio': 'Município', 'cultura': 'Cultura', 'sistema': 'Sistema', 'area_ha': 'Área (ha)', 'potencia_kw': 'Potência elétrica ativa (kW)', 'horas_dia': 'Operação diária (h)', 'dias_mes': 'Dias por mês', 'tarifa': 'Tarifa base (R$/kWh)', 'desconto': 'Desconto hipotético (%)', 'reducao_horas_pct': 'Redução hipotética do tempo (%)', 'melhoria_bomba_pct': 'Redução hipotética da potência (%)', 'rendimento_bomba': 'Rendimento informado da bomba (%)', 'rendimento_motor': 'Rendimento informado do motor (%)', 'meses_operacao_ano': 'Meses por ano', 'vazao_m3h': 'Vazão (m³/h)', 'altura_mca': 'Altura manométrica total (m)', 'horas_elegiveis_desconto': 'Horas elegíveis ao desconto (h/dia)', 'origem_dados': 'Origem declarada', 'observacoes_dados': 'Observações dos dados'}

def scenarios_dataframe(scenarios):
    return pd.DataFrame([{
        'Cenário':s.cenario,'Potência elétrica (kW)':s.potencia_kw,'Horas/dia':s.horas_dia,
        'Consumo anual (kWh)':s.consumo_anual_kwh,'Custo anual (R$)':s.custo_anual_rs,
        'Volume anual (m³)':s.volume_anual_m3,'kWh/1.000 m³':s.consumo_especifico_kwh_1000m3,
        'kWh/ha.ano':s.consumo_ha_kwh_ano,'R$/ha.ano':s.custo_ha_rs_ano,
        'Economia anual (R$)':s.economia_anual_rs,'Economia de custo (%)':s.economia_percentual,
        'Energia com desconto (kWh/ano)':s.energia_com_desconto_kwh_ano,
        'Energia sem desconto (kWh/ano)':s.energia_sem_desconto_kwh_ano,
        'Tarifa média efetiva (R$/kWh)':s.tarifa_efetiva
    } for s in scenarios])

def technical_values(data):
    out={'Rendimento global informado (%)':eficiencia_global(data.rendimento_bomba,data.rendimento_motor)*100}
    if data.vazao_m3h is not None:
        ph=potencia_hidraulica_kw(data.vazao_m3h,data.altura_mca)
        out.update({'Potência hidráulica (kW)':ph,
            'Potência elétrica estimada pelos rendimentos (kW)':potencia_eletrica_estimativa_kw(data.vazao_m3h,data.altura_mca,data.rendimento_bomba,data.rendimento_motor),
            'Rendimento implícito Ph/Pe informado (%)':100*(ph/data.potencia_kw)})
    return out

def sources_dataframe():
    return pd.read_csv(ROOT/'database/BCCI/BCCI_07_referencias.csv').fillna('')

def generate_text_report(data,scenarios,diagnosis):
    lines=['EFICIAGRO V3.2.2 — VERIFICAÇÃO COMPUTACIONAL',
        'Emissão UTC: '+datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'Origem declarada: '+data.origem_dados,
        'Menor custo simulado: '+diagnosis['melhor_cenario'],
        'Não é recomendação automática de implantação.','\nENTRADAS']
    lines += [f'{k}: {v}' for k,v in data.to_dict().items()]
    lines += ['\nINDICADORES']+[f'{k}: {v}' for k,v in technical_values(data).items()]
    lines += ['\nCENÁRIOS',scenarios_dataframe(scenarios).to_string(index=False),'\nLIMITAÇÕES']
    lines += diagnosis['alertas']
    lines += ['\nINVESTIMENTOS E PAYBACK (meses)', str(diagnosis.get('investimentos', 'Não informado')), str(diagnosis.get('paybacks_meses', 'Não informado'))]
    lines += ['\nORIENTAÇÕES']+[r['recomendacao']+' Fontes: '+r['referencias'] for r in diagnosis['recomendacoes']]
    lines += ['\nREFERÊNCIAS',sources_dataframe().to_string(index=False)]
    return '\n'.join(lines)

def _safe_cell(v):
    return "'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v

def generate_excel_report(data,scenarios,diagnosis,investimentos=None,paybacks=None):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    buf=io.BytesIO()
    df=scenarios_dataframe(scenarios)
    df['Investimento (R$)']=[(investimentos or {}).get(s.cenario) for s in scenarios]
    df['Payback simples (meses)']=[(paybacks or {}).get(s.cenario) for s in scenarios]
    sheets={'Metadados':pd.DataFrame({'Campo':['Versão','Emissão UTC','Natureza'], 'Valor':['3.2.2',datetime.now(timezone.utc).isoformat(timespec='seconds'),'Protótipo computacional; sem validação em campo']}),'Cenários':df,'Entradas':pd.DataFrame([(INPUT_LABELS.get(k,k),v) for k,v in data.to_dict().items()],columns=['Parâmetro','Valor']),
        'Indicadores':pd.DataFrame(technical_values(data).items(),columns=['Indicador','Valor']),
        'Limitações':pd.DataFrame({'Observação':diagnosis['alertas']}),
        'Orientações':pd.DataFrame(diagnosis['recomendacoes']), 'Referências':sources_dataframe()}
    with pd.ExcelWriter(buf,engine='openpyxl') as writer:
        for name,frame in sheets.items():
            frame=frame.map(_safe_cell)
            frame.to_excel(writer,index=False,sheet_name=name)
            ws=writer.sheets[name]; ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
            for cell in ws[1]:
                cell.font=Font(bold=True,color='FFFFFF'); cell.fill=PatternFill('solid',fgColor='245B44')
                cell.alignment=Alignment(wrap_text=True,vertical='center')
            ws.row_dimensions[1].height=44
            for col in range(1,ws.max_column+1):
                ws.column_dimensions[get_column_letter(col)].width=42 if col==1 else 25
            if name in ['Limitações','Referências','Orientações']:
                for col in range(1,ws.max_column+1): ws.column_dimensions[get_column_letter(col)].width=45
            for row in ws.iter_rows(min_row=2):
                for cell in row:
                    cell.alignment=Alignment(wrap_text=True,vertical='top')
                    if isinstance(cell.value,(int,float)): cell.number_format='#,##0.0000'
            for row in ws.iter_rows():
                for cell in row: cell.border=Border(*( [Side(style='thin',color='D9D9D9')]*4 ))
    buf.seek(0); return buf

def generate_pdf_report(data,scenarios,diagnosis,output_dir='exports',investimentos=None,paybacks=None):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
    from uuid import uuid4
    output=Path(output_dir); output.mkdir(parents=True,exist_ok=True)
    path=output/f'EficiAgro_{uuid4().hex[:10]}.pdf'
    import reportlab
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    fontdir=Path(reportlab.__file__).parent/'fonts'
    for name,filename in [('EficiSans','Vera.ttf'),('EficiSansBold','VeraBd.ttf')]:
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name,str(fontdir/filename)))
    styles=getSampleStyleSheet()
    for style in styles.byName.values():
        style.fontName='EficiSansBold' if style.name.startswith(('Heading','Title')) else 'EficiSans'
    styles['BodyText'].fontSize=8.5;styles['BodyText'].leading=11
    story=[]
    def para(s,style='BodyText'): return Paragraph(escape(str(s)),styles[style])
    def add(s,style='BodyText'): story.append(para(s,style));story.append(Spacer(1,6))
    def table(rows,widths):
        t=Table([[para(v) for v in row] for row in rows],colWidths=widths,repeatRows=1,splitInRow=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E6EDE8')),
            ('GRID',(0,0),(-1,-1),.4,colors.lightgrey),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(t);story.append(Spacer(1,12))
    add('EficiAgro V3.2.2','Title');add('Comparação condicional de energia e custos','Heading2')
    add('Emissão UTC: '+datetime.now(timezone.utc).isoformat(timespec='seconds'))
    add(f'Propriedade: {data.propriedade} | Município: {data.municipio}')
    add(f'Origem declarada: {data.origem_dados}. {data.observacoes_dados}')
    add('Menor custo simulado: '+diagnosis['melhor_cenario']+'. Não representa recomendação automática de implantação.')
    add('Entradas e indicadores','Heading2')
    table([['Parâmetro','Valor']]+[[INPUT_LABELS.get(k,k),v if v is not None else 'Não informado'] for k,v in data.to_dict().items() if k not in ['propriedade','municipio','observacoes_dados']],[300,207])
    table([['Indicador','Valor']]+[[k,f'{v:.6f}'] for k,v in technical_values(data).items()],[350,157])
    story.append(PageBreak());add('Comparação de cenários','Heading2')
    table([['Cenário','Energia anual (kWh)','Custo anual (R$)','Volume anual (m³)','kWh/1.000 m³']]+[[s.cenario,f'{s.consumo_anual_kwh:.2f}',f'{s.custo_anual_rs:.2f}',f'{s.volume_anual_m3:.2f}' if s.volume_anual_m3 is not None else 'Não informado',f'{s.consumo_especifico_kwh_1000m3:.2f}' if s.consumo_especifico_kwh_1000m3 is not None else 'Não calculado'] for s in scenarios],[143,91,91,91,91])
    table([['Cenário','Investimento (R$)','Payback simples (meses)']]+[[s.cenario,f'{investimentos[s.cenario]:.2f}' if investimentos and investimentos.get(s.cenario) is not None else 'Não informado',f'{(paybacks or {})[s.cenario]:.2f}' if (paybacks or {}).get(s.cenario) is not None else 'Não aplicável'] for s in scenarios],[247,130,130])
    add('Payback linear com economia anual constante; não considera juros, inflação, manutenção, vida útil ou perdas produtivas. Investimento zero com economia positiva tem payback zero.')
    add('Hipóteses e limitações','Heading2')
    for msg in diagnosis['alertas']: add(msg)
    add('Orientações condicionais','Heading2')
    for rec in diagnosis['recomendacoes']: add(rec['recomendacao']+' Fontes: '+rec['referencias'])
    story.append(PageBreak());add('Referências consultáveis','Heading2')
    for _,r in sources_dataframe().iterrows(): add(f"{r['id']} — {r['referencia_completa']} {r['url']}")
    def footer(canvas,doc):
        canvas.setFont('EficiSans',8);canvas.drawRightString(A4[0]-44,24,f'EficiAgro V3.2.2 | {doc.page}')
    SimpleDocTemplate(str(path),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=40,bottomMargin=40).build(story,onFirstPage=footer,onLaterPages=footer)
    return str(path)
