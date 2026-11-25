from core.calculations import finite_number, integer_number, potencia_hidraulica_kw, eficiencia_global, potencia_eletrica_estimativa_kw
VALID_CULTURES = {'Café arábica', 'Café conilon'}
VALID_SYSTEMS = {'Gotejamento', 'Microaspersão'}
ORIGENS = {'Não documentada', 'Caso sintético', 'Estimativas do usuário', 'Medições/documentos declarados'}

def validate_inputs(data):
    errors = []
    if not isinstance(data.propriedade, str) or not data.propriedade.strip():
        errors.append('Informe o nome da propriedade.')
    for attr, limit in [('propriedade', 200), ('municipio', 200), ('observacoes_dados', 4000)]:
        value = getattr(data, attr)
        if not isinstance(value, str) or len(value) > limit or any(ord(c) < 32 and c not in '\t\n\r' for c in value):
            errors.append(f'{attr}: texto inválido ou acima de {limit} caracteres.')
    if not isinstance(data.cultura, str) or data.cultura not in VALID_CULTURES: errors.append('Cultura inválida.')
    if not isinstance(data.sistema, str) or data.sistema not in VALID_SYSTEMS: errors.append('Sistema inválido.')
    if not isinstance(data.origem_dados, str) or data.origem_dados not in ORIGENS: errors.append('Origem dos dados inválida.')
    limits = [('area_ha',0,None,True),('potencia_kw',0,None,True),('horas_dia',0,24,True),
              ('tarifa',0,None,True),('desconto',0,90,False),('reducao_horas_pct',0,50,False),
              ('melhoria_bomba_pct',0,40,False),('rendimento_bomba',0,100,True),
              ('rendimento_motor',0,100,True),('horas_elegiveis_desconto',0,8.5,False)]
    for attr,lo,hi,strict in limits:
        try: finite_number(getattr(data,attr), attr, lo, hi, strict)
        except ValueError as exc: errors.append(str(exc))
    for attr,hi in [('dias_mes',31),('meses_operacao_ano',12)]:
        try: integer_number(getattr(data,attr), attr, 1, hi)
        except ValueError as exc: errors.append(str(exc))
    for attr in ['vazao_m3h','altura_mca']:
        if getattr(data,attr) is not None:
            try: finite_number(getattr(data,attr), attr, strict=True)
            except ValueError as exc: errors.append(str(exc))
    if (data.vazao_m3h is None) != (data.altura_mca is None):
        errors.append('Informe vazão e altura manométrica em conjunto.')
    if errors: return errors
    if data.dias_mes * data.meses_operacao_ano > 365:
        errors.append('O calendário simplificado não pode exceder 365 dias/ano.')
    try:
        eficiencia_global(data.rendimento_bomba, data.rendimento_motor)
    except ValueError as exc: errors.append(str(exc))
    if data.vazao_m3h is not None:
        try:
            ph = potencia_hidraulica_kw(data.vazao_m3h,data.altura_mca)
            finite_number(ph, 'Potência hidráulica', strict=True)
            potencia_eletrica_estimativa_kw(data.vazao_m3h, data.altura_mca, data.rendimento_bomba, data.rendimento_motor)
            if data.potencia_kw < ph * (1-1e-12):
                errors.append('Potência elétrica inferior à potência hidráulica: rendimento implícito acima de 100%.')
            elif data.potencia_kw*(1-data.melhoria_bomba_pct/100) < ph*(1-1e-12):
                errors.append('A redução de potência proposta implica rendimento acima de 100%, mantendo vazão e HMT. Reduza a hipótese de melhoria.')
        except ValueError as exc: errors.append(str(exc))
    return errors

def input_warnings(data):
    messages = [
        'Resultados condicionais; não há validação de campo, metrológica ou agronômica.',
        'Potência elétrica ativa deve representar a operação; potência nominal no eixo não é equivalente.',
        'O custo inclui somente energia ativa pela tarifa informada; não reproduz a fatura completa.',
        'O modelo usa horas/dia e dias/mês constantes e calendário de até 365 dias.',
        'O menor custo simulado não comprova viabilidade técnica nem retorno econômico global.'
    ]
    if data.reducao_horas_pct:
        messages.append('Reduzir tempo reduz volume bombeado à vazão constante; o atendimento hídrico não é verificado.')
    if data.melhoria_bomba_pct:
        messages.append('Redução de potência é hipótese, mantendo vazão e HMT; requer comprovação do ponto de operação.')
    if data.desconto:
        messages.append('Desconto e horas elegíveis são hipóteses; enquadramento e escala devem ser confirmados com a distribuidora. Não são inferidos pelo município.')
    if data.vazao_m3h is not None:
        implied = potencia_hidraulica_kw(data.vazao_m3h, data.altura_mca) / data.potencia_kw
        declared = eficiencia_global(data.rendimento_bomba, data.rendimento_motor)
        if abs(implied-declared) > 0.01:
            messages.append(f"Rendimento implícito ({implied*100:.2f}%) difere do produto informado ({declared*100:.2f}%). Confira os dados; o limiar de 1 ponto percentual é apenas um alerta computacional, não critério metrológico.")
    if data.vazao_m3h is None:
        messages.append('Sem vazão e HMT, não é possível verificar a compatibilidade energética com o serviço hidráulico.')
    return messages
