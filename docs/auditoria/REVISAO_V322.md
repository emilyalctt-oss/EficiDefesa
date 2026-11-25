# EficiAgro 3.2.2 — candidato à defesa

Base: ZIP V3.2.1 recebido. Preservados os cinco cenários, dados sintéticos e identidade visual. Não houve validação de campo.

## Alterações
- Validação de textos, tipos, limites de comprimento e caracteres de controle; rejeição de rendimentos cujo produto não é representável e potência hidráulica positiva que sofre subfluxo.
- Payback rejeita inteiros não representáveis; limite de desconto do cenário coincide com a interface (90%). O auxiliar genérico de tarifa permanece com domínio até 100%.
- Relatórios distinguem economia de custo, registram versão e não confundem investimento ausente com investimento zero. Interface explicita o caráter de protótipo.
- Nove novos casos de regressão; teste de planilhas atualizado para exigir a nova aba de metadados.

## Evidência
95 testes aprovados; um módulo ignorado (dois testes Streamlit não executados). 25/25 comparações e 15/15 verificações internas; conjuntos sobrepostos. Python 3.13.5; versões efetivamente usadas em validation/results/ambiente.json. Instalação de Streamlit indisponível neste ambiente. As versões de dependências da distribuição original não foram todas verificadas. A fonte primária do exemplo de Gomes não foi reconferida; os valores de referência são os registrados anteriormente. BCCI preservada, sem nova auditoria bibliográfica externa.

## Defesa
Apresentar como desenvolvimento e verificação de protótipo, não como comprovação de economia real. O cenário combinado reduz energia em 20,8% e custo em aproximadamente 44,56%, sob hipóteses sintéticas; volume cai 10%. Desconto não reduz energia. Redução de tempo não melhora consumo específico. Redução de potência exige manutenção do serviço hidráulico, não comprovada em campo. Os rendimentos informados do exemplo (55,25% global) divergem do implícito (17,84%); o alerta é intencional, não uma medição. Não alterar os dados sem atualizar a monografia.

Antes da defesa: instalar dependências, executar todos os testes, conferir interface e exportações, publicar/testar se necessário, reconferir fontes primárias e alinhar objetivos, metodologia, tabelas e versão com a orientadora.
