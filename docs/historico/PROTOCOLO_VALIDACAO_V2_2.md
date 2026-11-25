
# Protocolo de Validação v2.2

## Validação matemática
Conferência manual das equações de energia, custo, indicadores por hectare, economia percentual e tarifa efetiva.

## Validação lógica
- aumento da potência aumenta consumo;
- aumento das horas aumenta consumo;
- aumento da tarifa aumenta custo, sem alterar consumo;
- desconto reduz custo, sem alterar consumo;
- redução de tempo reduz consumo e custo;
- redução simulada de potência reduz consumo e custo;
- área altera indicadores específicos, mas não o consumo total.

## Validação de entradas
Verificação de área, potência, horas, dias, tarifa, percentuais e rendimentos.

## Critério de aceite
Todos os testes automatizados devem ser aprovados e os casos numéricos devem coincidir com os resultados calculados manualmente, admitindo tolerância de arredondamento de 0,01.
