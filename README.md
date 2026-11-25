# EficiAgro V3.2.2

O EficiAgro é um protótipo computacional desenvolvido para auxiliar na análise do desempenho energético de sistemas de irrigação na cafeicultura. A ferramenta integra parâmetros hidráulicos, energéticos, operacionais e econômicos, possibilitando a comparação de diferentes cenários de funcionamento.

## Funcionalidades

- Estimativa do consumo de energia elétrica;
- Cálculo da potência hidráulica;
- Análise dos rendimentos do conjunto motobomba;
- Estimativa do volume de água bombeado;
- Cálculo de indicadores energéticos;
- Análise dos custos operacionais;
- Simulação de descontos tarifários;
- Comparação de cenários;
- Estimativa de economia financeira e payback simples;
- Consulta à base de conhecimento técnico;
- Exportação de relatórios em PDF, Excel e TXT.

## Cenários de análise

O programa considera cinco condições de operação:

1. Condição atual;
2. Aplicação de desconto tarifário;
3. Redução do tempo de funcionamento;
4. Redução hipotética da potência elétrica do conjunto motobomba;
5. Combinação das intervenções.

## Tecnologias utilizadas

- Python;
- Streamlit;
- Pandas;
- SQLite;
- Openpyxl;
- ReportLab;
- Pytest.

## Instalação e execução

Recomenda-se a utilização de um ambiente virtual dedicado.

Criação do ambiente:

```bash
python -m venv .venv
```

Ativação no Windows:

```bash
.venv\Scripts\activate
```

Ativação no Linux ou macOS:

```bash
source .venv/bin/activate
```

Instalação das dependências:

```bash
python -m pip install -r requirements.txt
```

Execução da aplicação:

```bash
python -m streamlit run app.py
```

Os valores apresentados inicialmente correspondem a um caso sintético. Para análises específicas, devem ser substituídos pelos dados do sistema avaliado.

A potência elétrica informada deve corresponder à potência ativa de entrada do conjunto motobomba, e não à potência nominal de eixo.

## Estrutura do projeto

| Arquivo ou diretório | Descrição |
|---|---|
| `app.py` | Interface da aplicação |
| `core/` | Modelos, cálculos, indicadores, cenários e exportações |
| `database/BCCI/` | Base de conhecimento técnico |
| `tests/` | Testes automatizados |
| `scripts/` | Rotinas de verificação numérica |
| `validation/` | Registros e resultados das verificações |
| `docs/` | Documentação técnica |
| `requirements.txt` | Dependências da aplicação |

## Verificação computacional

A verificação dos modelos implementados contempla testes automatizados, comparações numéricas e análise da consistência dos resultados.

Execução dos testes:

```bash
python -m pytest -q --junitxml=validation/results/pytest.xml
```

Reprodução das comparações numéricas:

```bash
python scripts/verify_numeric.py
```

Os dados de entrada, resultados, referências numéricas e tolerâncias adotadas encontram-se no diretório `validation/results/`.

A comparação com a literatura considera as potências hidráulica e elétrica apresentadas no Exemplo 6.1 de Gomes (2013), utilizando a altura manométrica total fornecida.

## Premissas do modelo

O consumo de energia elétrica é calculado a partir da potência elétrica ativa e do tempo de funcionamento.

A redução do tempo de operação, quando mantida a vazão, implica redução do volume de água bombeado, não representando necessariamente melhoria da eficiência energética.

Os cenários de redução da potência elétrica consideram condições hipotéticas de operação. A manutenção da vazão e da altura manométrica total deve ser verificada no sistema real.

A análise tarifária considera os parâmetros informados pelo usuário e o limite de até 8,5 horas diárias para aplicação do desconto. As condições de concessão do benefício devem ser verificadas junto à distribuidora de energia elétrica.

A análise econômica não calcula separadamente parcelas de demanda, encargos, tributos ou bandeiras tarifárias. O retorno do investimento é estimado pelo método do payback simples.

## Armazenamento de dados

O histórico de análises utiliza SQLite e permanece desabilitado por padrão.

Para habilitar o armazenamento em ambiente local e privado, deve-se definir a variável `EFICIAGRO_ENABLE_HISTORY=1`.

O banco de dados é armazenado em `database/eficiagro.db`, podendo ser definido outro caminho por meio da variável `EFICIAGRO_DB`.

A aplicação não dispõe de autenticação ou isolamento de dados entre usuários. O histórico não deve ser habilitado em ambientes públicos ou compartilhados.

## Limitações

O EficiAgro destina-se à análise energética preliminar e à comparação de cenários operacionais. Não realiza o dimensionamento hidráulico completo da instalação, o cálculo da evapotranspiração, a determinação da demanda hídrica da cultura ou a avaliação agronômica do manejo da irrigação.

Os resultados são condicionados aos dados de entrada e às hipóteses adotadas.

O protótipo foi submetido a verificações matemáticas, numéricas e computacionais, sem validação experimental em campo.

## Desenvolvimento

**Autora:** Emily Aderno Leite

**Orientadora:** Gabriele Costa Gonçalves Dantas

**Curso:** Engenharia de Energias

**Instituição:** Universidade Federal do Recôncavo da Bahia (UFRB)

**Ano:** 2026

**Versão:** 3.2.2
