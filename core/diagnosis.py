from core.indicators import executive_summary, power_per_ha_interpretation
from core.recommendations import generate_recommendations
from core.validation import input_warnings

def generate_diagnosis(data, scenarios):
    s=executive_summary(data,scenarios)
    return dict(status_economia=s['classificacao_economia'],
        mensagem='Comparação condicional de energia e custos; não constitui diagnóstico de campo.',
        melhor_cenario=s['melhor_cenario'],economia_anual=s['economia_anual'],
        economia_percentual=s['economia_percentual'],
        potencia_especifica_classificacao=power_per_ha_interpretation(0),
        confiabilidade=s['confiabilidade'],
        recomendacoes=[r.to_dict() for r in generate_recommendations(data,scenarios)],
        alertas=input_warnings(data))
