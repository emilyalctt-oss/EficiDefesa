# EficiAgro V3.1 — Revisão técnica e computacional

## Alterações principais

A V3.1 mantém o escopo do EficiAgro como ferramenta de apoio à decisão e corrige pontos metodológicos importantes.

1. A anualização do consumo e do custo deixa de assumir obrigatoriamente 12 meses e passa a utilizar o número de meses de operação informado pelo usuário.
2. O desconto tarifário permanece separado da redução física de energia: ele altera o custo, mas não o consumo.
3. O cenário de melhoria do conjunto motobomba é explicitamente tratado como hipótese de redução da potência elétrica, e não como resultado de auditoria.
4. A potência específica em kW/ha é mantida como indicador descritivo, sem classificação universal por faixas.
5. Foram adicionados dados hidráulicos opcionais (vazão e HMT) para estimativa de potência hidráulica, potência elétrica teórica, volume anual e consumo específico por volume.
6. A eficiência global informada é calculada pelo produto entre rendimento da bomba e rendimento do motor.
7. A suíte interna de validação foi ampliada para 15 verificações matemáticas e lógicas.
8. A aba Histórico foi corrigida para utilizar a guia correta.
9. O painel passou a distinguir economia financeira e redução física de consumo.

## Limitações preservadas

O EficiAgro não substitui projeto hidráulico, manejo agronômico, ensaio de conjunto motobomba, auditoria energética ou consulta à distribuidora. A redução simulada de potência, o desconto tarifário e os investimentos são hipóteses definidas pelo usuário.
