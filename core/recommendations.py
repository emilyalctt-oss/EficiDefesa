from dataclasses import dataclass, asdict

@dataclass
class Recommendation:
    codigo: str
    diagnostico: str
    recomendacao: str
    prioridade: str
    pontuacao: int
    justificativa: str
    referencias: str
    def to_dict(self): return asdict(self)

def generate_recommendations(data, scenarios):
    """Orientações condicionais, sem diagnóstico automático de eficiência."""
    rows=[('R001','Caracterização energética','Registrar a origem da potência elétrica, vazão e HMT no mesmo ponto de operação.','Os dados devem representar o mesmo serviço hidráulico.','REF011;REF017'),
          ('R002','Manutenção','Inspecionar filtragem, emissores, pressão e vazamentos conforme o projeto.','A manutenção é condição de operação; não garante percentual fixo de economia.','REF008;REF015')]
    if data.reducao_horas_pct:
        rows.append(('R003','Hipótese de redução do tempo','Confirmar atendimento hídrico antes de reduzir o tempo de operação.','Menor volume não significa ganho de eficiência energética.','REF002;REF003'))
    if data.melhoria_bomba_pct:
        rows.append(('R004','Hipótese de redução da potência','Confirmar por medições e curvas da bomba se a redução mantém vazão e HMT.','A redução foi informada pelo usuário, não estimada por auditoria.','REF011;REF017'))
    if data.desconto:
        rows.append(('R005','Hipótese tarifária','Confirmar elegibilidade, tarifa e escala de horas com a distribuidora.','O benefício é aplicado apenas às horas elegíveis informadas.','REF009;REF019'))
    return [Recommendation(c,d,r,'Sem hierarquização automática',0,j,ref) for c,d,r,j,ref in rows]
