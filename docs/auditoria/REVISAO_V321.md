# Revisão V3.2.1 — 25/11/2026

Base: ZIP enviado, commit indicado a9ec12ce74b1c86ec0caa8db3b5254d42dc612fc. Preservados os cinco cenários, identidade visual, BCCI e equações centrais.

## Alterações
- Validação de inteiros gigantes sem OverflowError e rejeição de custo anual subnormal arredondado a zero.
- Energia elegível limitada à energia total para evitar resíduo negativo por arredondamento.
- Alerta explícito de divergência entre rendimento informado e implícito; limiar de 1 ponto percentual é apenas heurística de aviso, não tolerância científica.
- Histórico SQLite desabilitado por padrão para implantação compartilhada; conexões fechadas explicitamente. Sem autenticação: habilitar apenas localmente.
- PDF preparado permanece disponível durante reruns da mesma análise; alteração das entradas invalida o download anterior. Tabelas PDF permitem divisão de linhas.
- Exportação Excel protege também prefixos de fórmula precedidos por espaços; relatório TXT inclui investimentos e paybacks quando disponíveis.
- Tratamento de erro no payback e identificação da versão atual.

## Evidências
Antes: 78 testes não relacionados à interface aprovados. Depois: 86 aprovados, 1 módulo ignorado (2 casos de interface). 25 comparações numéricas e 15 verificações internas aprovadas; há sobreposição. Compilação sintática bem-sucedida. Ambiente Python 3.13 e dependências efetivas em validation/results/ambiente.json. Streamlit não instalado; tentativa de instalação falhou. Não houve teste visual, teste de implantação ou instalação integral das versões fixadas. Os valores do exemplo de Gomes são reproduzidos do registro anterior, não reconferidos na fonte primária. A auditoria bibliográfica integral e a conferência com o documento final do TCC permanecem pendentes. Não há validação de campo.

## Antes da defesa
Instalar em ambiente Python 3.12, executar pytest sem módulos ignorados, abrir app, testar exportações e histórico privado, conferir resultados e bibliografia com o TCC. Não publicar dados privados. Não interpretar redução de tempo como ganho de eficiência.
