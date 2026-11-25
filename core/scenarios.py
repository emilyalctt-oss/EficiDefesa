from core.calculations import calculate_scenario

def generate_scenarios(data):
    from core.validation import validate_inputs
    errors = validate_inputs(data)
    if errors:
        raise ValueError("; ".join(errors))
    common = dict(
        dias_mes=data.dias_mes,
        tarifa=data.tarifa,
        area_ha=data.area_ha,
        meses_operacao_ano=data.meses_operacao_ano,
        vazao_m3h=data.vazao_m3h,
        horas_elegiveis_desconto=data.horas_elegiveis_desconto,
    )

    atual = calculate_scenario(
        "Atual", data.potencia_kw, data.horas_dia, **common
    )

    horario = calculate_scenario(
        "Horário com desconto",
        data.potencia_kw,
        data.horas_dia,
        desconto_pct=data.desconto,
        custo_atual=atual.custo_anual_rs,
        **common,
    )

    reducao = calculate_scenario(
        "Redução do tempo de operação",
        data.potencia_kw,
        data.horas_dia * (1 - data.reducao_horas_pct / 100.0),
        desconto_pct=0,
        custo_atual=atual.custo_anual_rs,
        **common,
    )

    # Cenário hipotético: a melhoria é representada como redução percentual
    # da potência elétrica requerida, informada pelo usuário.
    bomba = calculate_scenario(
        "Melhoria do conjunto motobomba",
        data.potencia_kw * (1 - data.melhoria_bomba_pct / 100.0),
        data.horas_dia,
        desconto_pct=0,
        custo_atual=atual.custo_anual_rs,
        **common,
    )

    combinado = calculate_scenario(
        "Cenário combinado",
        data.potencia_kw * (1 - data.melhoria_bomba_pct / 100.0),
        data.horas_dia * (1 - data.reducao_horas_pct / 100.0),
        desconto_pct=data.desconto,
        custo_atual=atual.custo_anual_rs,
        **common,
    )

    return [atual, horario, reducao, bomba, combinado]

def best_scenario(scenarios):
    return min(scenarios, key=lambda s: s.custo_anual_rs)
