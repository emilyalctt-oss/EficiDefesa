# EficiAgro V3.2.2

Ferramenta local de apoio à análise energética e comparação condicional de custos em irrigação de café. Não dimensiona a instalação, não calcula evapotranspiração, não verifica demanda hídrica e não certifica eficiência de campo.

## Instalação e uso

Ambiente verificado: Python 3.12. Recomendado ambiente virtual dedicado.

```bash
python -m venv .venv
```

Windows: `.venv\Scripts\activate`. Linux/macOS: `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Os valores iniciais são um caso sintético. Substitua-os por dados documentados antes de qualquer análise real. A potência solicitada é elétrica ativa na entrada, não potência nominal de eixo.

## Verificação reproduzível

Na pasta do projeto:

```bash
python -m pytest -q --junitxml=validation/results/pytest.xml
python scripts/verify_numeric.py
```

`validation/results` contém entradas, resultados, referências numéricas, tolerâncias e ambiente. A comparação publicada usa somente potências do Exemplo 6.1 de Gomes (2013), com HMT fornecida; não reproduz o dimensionamento de tubulações nem a anualização de 365 dias do livro.

## Como interpretar

- A energia usa potência elétrica declarada e tempo; a potência hidráulica e a potência elétrica estimada são indicadores separados.
- Menos tempo à vazão constante significa menos água. Não afirmar ganho de eficiência só pela redução de kWh.
- A redução de potência é hipótese; manter vazão e HMT precisa ser comprovado no conjunto real.
- A tarifa é uniforme fora das horas elegíveis. Benefício, percentual e escala devem ser confirmados com a distribuidora. O modelo adota até 8,5 h/dia; não cobre exceções regulatórias.
- O custo não contém parcelas de demanda, encargos, tributos ou bandeiras calculados separadamente. A tarifa inserida deve ter composição documentada e o desconto deve ser aplicável à parcela modelada.
- O menor custo simulado ignora investimento no ranking. O payback simples é apresentado separadamente; investimento zero e economia positiva resultam em zero meses, sem presumir ausência de outros custos.
- Não há classificação automática de confiabilidade, faixas universais de desempenho ou recomendação automática de investimento.

## Estrutura

`app.py`: interface. `core/`: modelos, validação, cálculos, cenários, indicadores, orientações, exportações, SQLite. `database/BCCI/`: base técnica consultável. `tests/`: regressão e integração. `scripts/`: reprodução dos resultados. `docs/`: decisões, auditoria e histórico.

## Histórico e privacidade

O histórico é local, em `database/eficiagro.db`, compatível com a estrutura anterior. Para outro caminho, defina a variável `EFICIAGRO_DB`. Não há autenticação ou isolamento multiusuário; não publicar uma instalação com dados de propriedades em servidor compartilhado sem adicionar esses controles. Exportações contêm os dados inseridos.

## Limites da entrega

Aprovação de testes é evidência das rotinas examinadas, não prova de ausência de defeitos. Não foram realizados ensaios de campo, medição de rendimento, avaliação com produtores ou homologação regulatória. A adequação editorial do TCC utiliza a Resolução CONAC/UFRB nº 053/2022. A modalidade é monografia. A divergência de espaçamento do resumo e as informações da banca precisam de conferência da autora e orientadora; consulte docs/auditoria/RELATORIO_REVISAO_V32.md.

## Enquadramento acadêmico atualizado

O EficiAgro V3.2 é um protótipo em aperfeiçoamento apresentado em monografia. O uso proposto é apoio à análise preliminar por profissionais técnicos e uso acompanhado por produtores. Benefícios de usabilidade e economia em campo ainda exigem avaliação. A auditoria em docs/auditoria/RELATORIO_REVISAO_V32.md registra a conferência bibliográfica de 5 nov. 2026.

## Revisão V3.2.1 — 25/11/2026

Histórico desabilitado por padrão. Para uso individual privado, defina `EFICIAGRO_ENABLE_HISTORY=1` (PowerShell: `$env:EFICIAGRO_ENABLE_HISTORY='1'`; Linux/macOS: `export EFICIAGRO_ENABLE_HISTORY=1`). Não habilite em servidor público. O banco vazio original foi retirado do pacote; será criado quando necessário. Os resultados anteriores estão em `validation/historico_v32`. A revisão atual executou 86 testes, com módulo de interface ignorado por falta de Streamlit (dois casos não executados). As versões fixadas originais foram preservadas, mas sua instalação não foi confirmada. Consulte `docs/auditoria/REVISAO_V321.md`.

## Revisão V3.2.2 — candidato à defesa

Consulte `docs/auditoria/REVISAO_V322.md`. Evidência atual: 95 testes aprovados, dois casos de interface não executados (um módulo ignorado), 25 comparações e 15 verificações internas aprovadas. O ambiente efetivo desta execução foi Python 3.13.5; o registro anterior de Python 3.12 é histórico. Não houve nova auditoria externa das referências nem validação de campo. Para a defesa, execute os comandos acima em ambiente com Streamlit instalado e confirme que não há testes ignorados.
