"""Indicadores descritivos; sem faixas universais ou pontuação de confiabilidade."""
def classify_economy(p):
    return 'Redução simulada' if p > 0 else ('Aumento simulado' if p < 0 else 'Sem variação')

def power_per_ha_interpretation(_p):
    return 'Indicador descritivo; depende das condições de operação'

def classify_reliability(data):
    # Nome preservado por compatibilidade; saída descreve origem, não qualidade.
    return data.origem_dados

def executive_summary(data, scenarios):
    atual=scenarios[0]
    best=min(scenarios,key=lambda s:s.custo_anual_rs)
    delta=atual.consumo_anual_kwh-best.consumo_anual_kwh
    return dict(consumo_anual=atual.consumo_anual_kwh,custo_anual=atual.custo_anual_rs,
        custo_ha=atual.custo_ha_rs_ano,melhor_cenario=best.cenario,
        economia_anual=best.economia_anual_rs,economia_percentual=best.economia_percentual,
        reducao_consumo_kwh=delta,reducao_consumo_percentual=delta/atual.consumo_anual_kwh*100,
        classificacao_economia=classify_economy(best.economia_percentual),
        confiabilidade=classify_reliability(data),horas_operacao_ano=atual.horas_operacao_ano)
