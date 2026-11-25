# Revisão e verificação — EficiAgro V3.2

Data: 1 de novembro de 2026. Escopo: texto do TCC, aplicação Python/Streamlit e evidências computacionais. Esta entrega é uma versão revisada para conferência da autora e orientadora; não representa validação experimental em propriedades.

## Correções por prioridade

| Prioridade | Problema | Tratamento realizado |
|---|---|---|
| Crítica | Desconto aplicado indistintamente ao consumo | Separação da energia em horas elegíveis e demais horas; limite de 8,5 h/dia e teste independente com R$ 11.340/ano. |
| Crítica | Entradas impossíveis ou não finitas | Rejeição de NaN, infinitos, rendimentos fora do domínio, calendário acima de 365 dias, vazão/HMT incompletas e potência elétrica inferior à hidráulica, inclusive após redução hipotética. |
| Crítica | Classificações sem sustentação | Retiradas pontuações arbitrárias de confiabilidade e faixas genéricas de eficiência; origem dos dados explicitamente declarada. |
| Crítica | Alegações além do implementado | Texto e interface delimitam comparação energética e tarifária. Retiradas alegações de cálculo de evapotranspiração, atendimento hídrico e eficiência comprovada em campo. |
| Alta | Confusão entre economia e eficiência | Redução do tempo também reduz volume; desconto não reduz energia; menor custo não equivale a melhor investimento. |
| Alta | Bibliografia inconsistente | Identificações corrigidas, fontes sem confirmação suficiente retiradas do suporte ativo, referências identificadas no código e na base técnica. |
| Alta | Resultados incompletos | Inseridos caso sintético, cinco cenários, equações, comparação publicada, payback e discussão dos limites. |
| Alta | Falta de evidência reproduzível | Testes automatizados, comparação Decimal independente, entradas JSON, resultados CSV, registro JUnit e ambiente documentado. |
| Média | Histórico e exportações | Persistência SQLite, recuperação integral, PDF com fontes incorporadas e Excel com proteção contra interpretação de texto como fórmula. |
| Média | Organização e apresentação | Referencial antes da metodologia; numeração, quadros, figura de arquitetura, conclusão e bibliografia reorganizados. |

## Atendimento aos 16 comentários gerais da orientadora

| Item | Resposta na versão revisada |
|---|---|
| 1 — Estrutura | Referencial na seção 4, metodologia na seção 5, resultados na seção 6. |
| 2 — Objeto | Seção 3 e Quadro 3.1 distinguem entradas, processamento e limites. |
| 3 — Conceitos | Desempenho energético é o termo abrangente; economia tarifária e rendimento são tratados separadamente. |
| 4 — Eficiência | Consumo por volume e rendimento implícito têm equações e limites; custo isolado não comprova eficiência. |
| 5 — Alinhamento | Questão, objetivos, implementação e conclusão limitados ao desenvolvimento e verificação computacional. |
| 6 — Contribuição | Comparação delimitada com CROPWAT/AquaCrop; sem alegação de superioridade ou originalidade global. |
| 7 — Repetição | Introdução e contextualização condensadas. |
| 8 — Bibliografia | Fontes específicas, identificadas e com endereço consultável; ressalvas de acesso registradas abaixo. |
| 9 — Teoria e ferramenta | Bombeamento, indicadores e custos ligados às equações e hipóteses implementadas. |
| 10 — Desenvolvimento | Requisitos, arquitetura, fluxo, entradas, saídas e persistência descritos. |
| 11 — Validação técnica | Entradas, valores esperados, tolerâncias, resultados e comandos de reprodução fornecidos. |
| 12 — Natureza dos testes | Verificação funcional e numérica separada de validação científica em campo. |
| 13 — Modelos | Unidades, fronteiras físicas, hipóteses e domínio computacional explicitados. |
| 14 — Indicadores | Correspondência entre texto, código e tabelas; funções não implementadas retiradas. |
| 15 — Público | Prioridade a estudantes e profissionais técnicos; uso direto por produtores requer orientação. |
| 16 — Limitações | Seção própria e alertas na interface/exportações. |

## Evidências executadas

- **80 casos pytest aprovados**, incluindo regressão, domínio numérico, consistência física, referências, SQLite, PDF, Excel e fluxos Streamlit AppTest.
- **15 verificações internas aprovadas**.
- **25 comparações numéricas aprovadas**, com aritmética Decimal independente e duas potências do Exemplo 6.1 de Gomes (2013, p. 163–166).
- O exemplo publicado produziu Ph = 30,5789472 kW contra 30,58 kW e Pe = 56,62768 kW contra 56,628 kW. Tolerâncias: 0,005 e 0,0005 kW, respectivamente.
- Caso sintético atual: 7.920 kWh/ano; R$ 7.524,00/ano; 51.840 m³/ano. Combinado: 6.272,64 kWh/ano; R$ 4.171,31/ano; 46.656 m³/ano. São hipóteses didáticas, não resultados de uma propriedade.
- DOCX renderizado e conferido visualmente; exportação PDF também inspecionada. O AppTest verifica execução simulada, não homologação visual em todos os navegadores.

As contagens se sobrepõem: a suíte interna também é chamada por testes automatizados. Não somar os conjuntos para alegar experimentos independentes. Testes aprovados não provam ausência de defeitos.

## Auditoria bibliográfica

A base ativa possui 11 referências. A bibliografia do TCC inclui também páginas oficiais da FAO e documentação de software. A identificação de uma obra não significa conferência integral de todas as suas páginas: os usos foram delimitados ao conteúdo efetivamente consultado.

| Fonte ou problema original | Decisão e alcance |
|---|---|
| ANA — Atlas Irrigação | Identidade institucional confirmada; uso contextual, sem coeficientes de diagnóstico. |
| Cararo e Dias, 2015 | Autoria e capítulo identificados no repositório Embrapa; contexto de irrigação de café. |
| Rocha et al., 2016 | Circular Técnica 32 identificada; condições do Cerrado, sem extrapolação automática. |
| CT 48 da Embrapa | Corrigida para Circular Técnica 48, Veiga et al., 2021, sobre café canéfora. |
| SENAR 251 | Pendência de acesso resolvida em 5 nov. 2026: texto oficial consultado, ano 2019 e ISBN confirmados; uso conceitual, sem limiares quantitativos. |
| ANEEL | Página oficial de modalidades tarifárias para contextualização. Não alegar implementação integral da REN 1.000/2021. |
| MME 137/2026 | Texto oficial consultado, art. 2º. O programa representa limite diário de horas; não verifica escala, enquadramento ou direito ao benefício. |
| Gomes | Obra de irrigação identificada como edição de 2013 no LENHS/UFPB; texto consultado nas p. 163–166 e 208–209. Não confundir com livro de bombeamento de 2009. |
| Schwankl | Capítulo sobre pistache; somente princípios gerais de componentes e manutenção. |
| Lima et al., 2009 | Artigo sobre pivô central; não usado para limites universais de gotejamento. |
| Loureiro et al., 2024 | Volume 42, p. 745–768; DOI com 2023 corresponde à publicação antecipada. Contexto de sistemas coletivos. |
| REF018 | Identificador sem entrada bibliográfica na versão anterior; retirado do código. |
| Scapin / REF012 | Confirmação primária insuficiente; retirado do suporte ativo, sem afirmar inexistência da obra. |
| FAO / REF014 | Identificação do documento não resolvida; retirado do suporte ativo. |
| REF005, REF006, REF007, REF010 e REF013 | Retiradas da base ativa por não serem necessárias ao escopo revisado; remoção não significa que as publicações sejam inválidas. |
| Carvalho, Turban e Bernardo | Dados bibliográficos inconsistentes na redação anterior; obras não utilizadas na nova argumentação. Não manter entradas apenas para aumentar a lista. |
| Silvestre e Ribeiro | Retirados da fundamentação operacional: os objetos dos estudos não verificam o modelo energético implementado. |

A lista original da BCCI foi preservada em `docs/auditoria/referencias_v31_original.csv`. O arquivo vigente `database/BCCI/BCCI_07_referencias.csv` contém endereços e escopo de verificação por fonte. Documentos antigos estão em `docs/historico` e não descrevem a versão atual.

## Reprodução

Na pasta do projeto, com Python 3.12 e ambiente virtual ativado:

```bash
python -m pip install -r requirements.txt
python -m pytest -q --junitxml=validation/results/pytest.xml
python scripts/verify_numeric.py
python -m streamlit run app.py
```

Evidências: `validation/results/pytest.xml`, `comparacao_numerica.csv`, `cenarios_caso_sintetico.csv`, `caso_sintetico.json`, `suite_interna.json`, `resumo.json` e `ambiente.json`. O README explica instalação em Windows e Linux/macOS. O ambiente registra as dependências diretas verificadas; não representa teste em todos os sistemas operacionais.

## Pontos que dependem de dados ou conferência externa

1. **Autora e orientadora:** conferir a redação, título, autoria e adequação à modalidade de TCC exigida. A Resolução CONAC/UFRB nº 053/2022 foi localizada no portal oficial e utilizada na adequação editorial. A modalidade monografia foi confirmada pela autora nesta conversa; conferir eventuais instruções complementares da turma. Não se declara homologação institucional.
2. **Validação em campo:** não realizada. Para acrescentá-la seriam necessários dados medidos, instrumentos e incertezas, protocolo de coleta e critérios de comparação. Não substituir esses dados por números inventados.
3. **Aplicação real:** confirmar potência ativa, vazão e HMT no mesmo ponto de operação; atendimento hídrico; orçamento e condições tarifárias com a distribuidora. Os 65%/85% iniciais são hipóteses e não são coerentes com o rendimento implícito do exemplo; essa diferença está exposta no TCC como limitação dos dados sintéticos.
4. **Publicação da aplicação:** versão local e individual, sem autenticação. Implantação multiusuário exigiria controle de acesso e tratamento dos dados armazenados.

O texto e o código estão alinhados ao estudo computacional documentado. A entrega não afirma economia observada em campo, aprovação da banca ou validação agronômica.


## Continuidade — adequação institucional

Foi consultada a [Resolução CONAC/UFRB nº 053/2022](https://ufrb.edu.br/soc/components/com_chronoforms5/chronoforms/uploads/resolucao/20220427103934_RESOLUCAO__53_TCC_Eng_de_Energias_-_com_alteracoes_assinado.pdf), que aparece como regulamento de TCC de Engenharia de Energias no portal da PROGRAD. Consulta em 1 nov. 2026. A busca não demonstrou a existência de instruções complementares específicas da turma.

Aplicados: papel A4; margem esquerda de 3 cm e demais margens de 2 cm; texto em Times New Roman 12 e espaçamento 1,5; numeração central inferior desde a capa; capa e folha de rosto; folha de aprovação para preenchimento real; resumo e abstract; sumário; numeração de figura, quadros, tabelas e equações por capítulo. Tabelas, legendas, fontes e referências receberam espaçamento compacto para leitura. Referências foram posicionadas antes do apêndice.

**Divergência do documento normativo:** os anexos VIII/IX indicam mínimo de 400 palavras e espaçamento 1,5; o anexo X indica até 400 palavras, uma folha e espaço simples para o resumo. Foram adotadas 400 palavras em cada idioma, por contagem de palavras separadas por espaços, e espaço simples para preservar uma página. Essa escolha editorial precisa ser confirmada pela orientação; não é possível cumprir simultaneamente as duas instruções de espaçamento.

**Sumário:** os números correspondem à renderização conferida. É um sumário estático; alterações posteriores no texto exigem atualização da paginação.

**Folha de aprovação:** data, examinadores e assinaturas não foram inventados. Preencher com os dados reais após definição da banca e aprovação. O ano 2026 acompanha a versão atual e deve ser ajustado se o depósito ocorrer em outro ano. A titulação acadêmica da orientadora não foi presumida.

**Modalidade:** a resolução admite diferentes formas de TCC. A organização pré-textual foi aplicada como preparação acadêmica; ela não constitui decisão do colegiado sobre o enquadramento deste trabalho. O texto enviado inicialmente tinha apresentação semelhante a artigo; confirmar a modalidade antes do depósito.

**Defesa e depósito:** a resolução prevê apresentação de 20 a 30 minutos e entrega após a aprovação. Confirmar os procedimentos administrativos atuais com o curso. Para uma exposição de 25 minutos, distribuir aproximadamente 3 minutos para problema e objetivo, 5 para modelo e hipóteses, 5 para demonstração do programa, 8 para resultados e verificações e 4 para limites e conclusão. Mostrar que desconto altera custo, redução de tempo também reduz água e comparação sintética não representa economia medida.

O link de REF008 passou a apontar para o catálogo oficial acessível do SENAR, mantendo explícita a limitação de acesso ao texto integral. Os cálculos da aplicação não foram alterados nesta etapa.

## Fechamento desta etapa — 5 nov. 2026

O documento institucional contém 29 páginas, conferidas visualmente, com 10 tabelas e uma figura. Foram corrigidas as remissões internas e a largura da coluna de identificação das equações. O sumário corresponde à paginação renderizada; alterações no Word podem exigir atualização.

As evidências anteriores de 80 testes automatizados, 15 verificações internas e 25 comparações numéricas foram preservadas. Nesta etapa editorial não houve nova execução da suíte completa; o teste específico de integridade das referências passou após a atualização do endereço do SENAR (validation/results/referencia_atualizada.xml). Não houve alteração nas rotinas de cálculo.

Os documentos posteriores de auditoria e prioridades foram consultados. Suas pendências relativas à indisponibilidade do ZIP descrevem aquela revisão editorial, não ausência de evidências neste pacote. A leitura integral de todas as obras não é declarada: o alcance de cada conferência e as restrições de acesso permanecem registrados nesta auditoria.

Prioridades restantes: (1) confirmar com a orientadora a modalidade de entrega e o tratamento da divergência de espaçamento do resumo; (2) preencher os dados reais da banca e da aprovação; (3) ensaiar a demonstração no computador da defesa, seguindo o README; (4) obter aceite do escopo computacional e das limitações. Validação em campo permanece não realizada e exigiria um protocolo e dados próprios.

## Revisão bibliográfica e justificativa consolidada em 5 nov. 2026

Esta seção atualiza as pendências históricas acima. Modalidade confirmada: **monografia**. O EficiAgro é apresentado como **protótipo em aperfeiçoamento**. A justificativa, o problema, os objetivos, a comparação de ferramentas, a discussão e a conclusão foram alinhados à integração de variáveis para análise preliminar. O capítulo 7 contém as etapas futuras e suas condições de avaliação. A nova renderização tem 33 páginas.

A conferência abrangeu as **20 entradas da bibliografia da monografia**, com exame dos metadados e do conteúdo necessário aos usos mantidos. Isso não equivale a leitura integral de todos os livros nem a revisão sistemática de toda a literatura. A base operacional BCCI permanece com 11 entradas; as demais referências sustentam o texto acadêmico. Afirmações sobre possíveis usos e etapas futuras são propostas da pesquisa, não resultados atribuídos às fontes ou observados em usuários.

### Matriz de conferência das referências utilizadas

| Fonte | Local efetivamente conferido e aplicação | Decisão ou limite |
|---|---|---|
| ANA, 2021 | Catálogo oficial, sumário e página do Atlas no SNIRH. | Identidade, edição e escopo nacional confirmados; o texto não utiliza números do Atlas. |
| ANEEL, 2022 | Página Modalidades Tarifárias, grupos A e B. | Corrigido s.d. para 2022, conforme data da página; não confundir com regra completa de faturamento. |
| Bolfe, Jorge e Sanches, 2021 | Artigo no repositório Embrapa; identificação, metodologia p. 23–24 e considerações finais p. 31–32. | Sustenta barreiras de adoção digital. Consulta on-line, sem generalizar sua amostra a todos os produtores. |
| Bonneville Power Administration, s.d. | Página Irrigation Pump Testing, avaliação e experiência exigida do executor. | Sustenta necessidade de dados e capacidade técnica; benefícios e regras do programa norte-americano não são transferidos ao Brasil. |
| Brasil/MME, 2026 | Portaria 137/2026, arts. 1º–3º, texto oficial de duas páginas. | Confirma 8h30 e definição de escala; não assegura elegibilidade, percentual ou economia para uma propriedade. Busca adicional não constitui parecer de vigência jurídica. |
| Cararo e Dias, 2015 | Registro Embrapa e PDF do capítulo; tópicos manejo da irrigação e considerações finais. | O catálogo informa p. 311–345; o PDF separado mostra numeração impressa 309–343. Mantida a faixa catalográfica na referência, sem atribuir páginas pontuais à citação no corpo. |
| FAO, s.d.a | About AquaCrop, descrição, aplicações e público. | Modelo de resposta produtiva à água para culturas herbáceas; não alegar aplicação direta ao café. |
| FAO, s.d.b | CROPWAT, descrição e recursos. | Caracterização documental de necessidades hídricas e programação; sem execução comparativa. |
| Gomes, 2013 | Catálogo LENHS/UFPB e exemplar digital, folha de rosto, ficha, p. 163–166 e 208–209. | Ano e obra confirmados. Exemplo 6.1: Q 48 L/s, H 64,94 m, rendimentos 60%/90%; potências 30,58 e 56,628 kW. Há aparente erro tipográfico 30,56 no numerador da potência mecânica; não foi adotado no cálculo. |
| Lima et al., 2009 | Artigo completo disponível na SciELO, identificação, resumo e análise de perdas. | DOI confirmado; uso conceitual restrito ao contexto de pivô central, sem transportar percentuais. |
| Loureiro et al., 2024 | Texto aberto da editora; resumo, metodologia de balanços, indicadores e conclusões. | Publicação on-line em 2023 e volume de 2024; uso de abordagem sistêmica, sem equivalência entre sistemas coletivos e o protótipo. |
| pytest, s.d. | Documentação oficial, apresentação do framework. | Fundamenta testes automatizados; resultados de aprovação provêm dos arquivos de teste do projeto. |
| Python Software Foundation, s.d. | Documentação sqlite3 da série Python 3.12. | URL fixada na série do ambiente documentado; fundamenta banco sem servidor separado, não certifica segurança da aplicação. |
| Rocha et al., 2016 | Registro e PDF da Circular Técnica 32, p. 3–4. | Manejo e coeficientes de cafeeiro no Cerrado; não implementados como coeficientes universais. |
| Schwankl, s.d. | PDF institucional, componentes e funcionamento, páginas impressas 55–56. | Autoria e título confirmados; data não identificada no documento, preservado s.d.; contexto de pistache explicitado. |
| SENAR, 2019 | PDF oficial CNA/SENAR, ficha, componentes, orientação técnica e manutenção p. 46–49. | Acesso antes bloqueado resolvido; ano, coleção 251, 55 p. e ISBN 978-85-7664-215-2 confirmados. |
| Streamlit, s.d. | Documentação oficial AppTest. | Simulação por API, distinta de operação visual de navegador e teste de usabilidade. |
| U.S. Department of Energy, 2006 | Sourcebook, identificação da 2ª edição, seção sobre abordagem sistêmica e seção 3, p. 55. | Sustenta interação entre componentes e demanda; contexto industrial, sem transpor percentuais de economia. |
| U.S. Department of Energy, s.d. | Página MEASUR, seção Pumping System Assessments. | Incluída ferramenta energética existente para evitar falsa alegação de ineditismo; comparação documental, sem benchmark. |
| Veiga et al., 2021 | PDF Embrapa, capa, autoria e informações gerais. | Circular Técnica 48, café canéfora no Cerrado; não sustenta ganho energético medido do software. |

### Lacuna, usuários e evidência

A lacuna é definida como integração aplicada de dados e modelos em um fluxo reproduzível para o problema delimitado. Não se afirma inexistência de ferramentas semelhantes: MEASUR integra avaliações energéticas, CROPWAT trata manejo hídrico e AquaCrop modela resposta produtiva à água. O atendimento da lacuna foi demonstrado no nível funcional e numérico do protótipo. A necessidade de mercado, a superioridade sobre outras soluções e a indispensabilidade não foram demonstradas.

Engenheiros e projetistas são públicos prioritários por aderência das tarefas às entradas técnicas; extensionistas podem mediar a análise junto aos produtores; pequenos produtores podem participar do uso acompanhado quando necessário. Essa segmentação é uma inferência de projeto, não resultado de entrevistas. Eficiência do processo de análise, facilidade de uso e melhoria da decisão são hipóteses a testar.

Desenvolvimentos futuros foram ligados às limitações atuais: medição e comparação em campo; curvas de bombas e redes; demanda hídrica e séries temporais; faturamento e análise econômica mais completos; avaliação de tarefas com usuários; instalação, acessibilidade e proteção dos dados. Cada ampliação exige novos critérios de verificação.

### Referências completas e endereços consultados

- AGÊNCIA NACIONAL DE ENERGIA ELÉTRICA (ANEEL). Modalidades tarifárias. Brasília, DF: ANEEL, 2022. Disponível em: https://www.gov.br/aneel/pt-br/assuntos/tarifas/entenda-a-tarifa/modalidades-tarifarias/. Acesso em: 5 nov. 2026.

- AGÊNCIA NACIONAL DE ÁGUAS E SANEAMENTO BÁSICO (ANA). Atlas irrigação: uso da água na agricultura irrigada. 2. ed. Brasília, DF: ANA, 2021. Disponível em: https://www.snirh.gov.br/portal/centrais-de-conteudos/central-de-publicacoes/atlas-irrigacao_2-ed.pdf/view. Acesso em: 5 nov. 2026.

- BOLFE, E. L.; JORGE, L. A. de C.; SANCHES, I. D. Tendências, desafios e oportunidades da Agricultura Digital no Brasil. Revista Eletrônica Competências Digitais para Agricultura Familiar, v. 7, n. 2, p. 15–36, 2021. Disponível em: https://www.alice.cnptia.embrapa.br/alice/handle/doc/1138840. Acesso em: 5 nov. 2026.

- BONNEVILLE POWER ADMINISTRATION. Irrigation Pump Testing. s.d. Disponível em: https://www.bpa.gov/energy-and-services/conservation/agricultural/irrigation-pump-testing. Acesso em: 5 nov. 2026.

- BRASIL. Ministério de Minas e Energia. Portaria Normativa MME nº 137, de 8 de junho de 2026. Estabelece diretrizes para a concessão dos descontos especiais nas tarifas de energia elétrica aplicáveis à irrigação e aquicultura. Brasília, DF, 2026. Disponível em: https://www.gov.br/mme/pt-br/acesso-a-informacao/legislacao/portarias/2026/portaria-normativa-mme-n-137-2026.pdf. Acesso em: 5 nov. 2026.

- CARARO, D. C.; DIAS, A. F. de S. Irrigação em cafeeiros. In: MARCOLAN, A. L.; ESPINDULA, M. C. (ed.). Café na Amazônia. Brasília, DF: Embrapa, 2015. cap. 14, p. 311-345. Disponível em: https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1040722. Acesso em: 5 nov. 2026.

- FOOD AND AGRICULTURE ORGANIZATION OF THE UNITED NATIONS (FAO). About AquaCrop. Rome: FAO, s.d.a. Disponível em: https://www.fao.org/aquacrop/overview/about-aquacrop/en. Acesso em: 5 nov. 2026.

- FOOD AND AGRICULTURE ORGANIZATION OF THE UNITED NATIONS (FAO). CROPWAT. Rome: FAO, s.d.b. Disponível em: https://www.fao.org/land-water/resources/tools/software/cropwat/en. Acesso em: 5 nov. 2026.

- GOMES, H. P. Sistemas de irrigação: eficiência energética. João Pessoa: Editora da UFPB, 2013. 281 p. Catálogo institucional: https://www.ct.ufpb.br/lenhs/publicacoes/livros/. Texto consultado: https://www.bibliotecaagptea.org.br/agricultura/irrigacao/livros/SISTEMAS%20DE%20IRRIGACAO%20EFICIENCIA%20ENERGETICA.pdf. Acesso em: 5 nov. 2026.

- LIMA, A. C.; GUIMARÃES JR., S. C.; FIETZ, C. R.; CAMACHO, J. R. Avaliação e análise da eficiência energética na irrigação em sistemas pivô central. Revista Brasileira de Engenharia Agrícola e Ambiental, v. 13, n. 4, p. 499-505, 2009. DOI: 10.1590/S1415-43662009000400020. Disponível em: https://www.scielo.br/j/rbeaa/a/Kc6B9vdSwgDMgh58nLYg8bP/. Acesso em: 5 nov. 2026.

- LOUREIRO, D.; BECEIRO, P.; FERNANDES, E.; ALEGRE, H.; COVAS, D. Energy efficiency assessment in collective irrigation systems using water and energy balances: methodology and application. Irrigation Science, v. 42, p. 745-768, 2024. DOI: https://doi.org/10.1007/s00271-023-00891-6.

- PYTEST DEVELOPERS. pytest documentation. s.d. Disponível em: https://docs.pytest.org/en/stable/. Acesso em: 5 nov. 2026.

- PYTHON SOFTWARE FOUNDATION. sqlite3 — DB-API 2.0 interface for SQLite databases. Python 3.12 documentation. s.d. Disponível em: https://docs.python.org/3.12/library/sqlite3.html. Acesso em: 5 nov. 2026.

- ROCHA, O. C.; GUERRA, A. F.; RODRIGUES, G. C.; BARTHOLO, G. F.; VEIGA, A. D. Coeficientes técnicos para irrigação do cafeeiro no Cerrado. Planaltina, DF: Embrapa Cerrados, 2016. Circular Técnica 32. Disponível em: https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1061432. Acesso em: 5 nov. 2026.

- SCHWANKL, L. J. Microirrigation systems. University of California, Agriculture and Natural Resources, s.d. Disponível em: https://ucanr.edu/sites/default/files/2011-02/73686.pdf. Acesso em: 5 nov. 2026.

- SERVIÇO NACIONAL DE APRENDIZAGEM RURAL (SENAR). Irrigação: manejo e gestão em sistema localizado. Brasília: Senar, 2019. 55 p. Coleção Senar, 251. ISBN 978-85-7664-215-2. Disponível em: https://www.cnabrasil.org.br/storage/arquivos/251-IRRIGAC387C383O_NOVO_2022-06-03-142856_radj.pdf. Acesso em: 5 nov. 2026.

- STREAMLIT. Streamlit’s native app testing framework. Streamlit documentation, s.d. Disponível em: https://docs.streamlit.io/develop/concepts/app-testing. Acesso em: 5 nov. 2026.

- U.S. DEPARTMENT OF ENERGY. Improving Pumping System Performance: A Sourcebook for Industry. 2. ed. 2006. DOE/GO-102006-2079. Disponível em: https://www.energy.gov/sites/default/files/2014/05/f16/pump.pdf. Acesso em: 5 nov. 2026.

- U.S. DEPARTMENT OF ENERGY. MEASUR. s.d. Disponível em: https://www.energy.gov/cmei/ito/measur. Acesso em: 5 nov. 2026.

- VEIGA, A. D.; GUERRA, A. F.; BARTHOLO, G. F.; ROCHA, O. C.; RODRIGUES, G. C.; AMABILE, R. F.; CELESTINO, S. M. C. Recomendações técnicas para o cultivo irrigado do café canéfora no Cerrado. Planaltina, DF: Embrapa Cerrados, 2021. Circular Técnica 48. Disponível em: https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1135273/1/CT-48-web.pdf. Acesso em: 5 nov. 2026.

A conferência bibliográfica não implica garantia de aprovação acadêmica. Permanecem a confirmação do espaçamento do resumo, os dados reais da banca e a avaliação final da orientadora. Não houve alteração das rotinas numéricas nesta revisão.

### Fechamento desta revisão

Os dois testes direcionados à integridade das referências foram executados novamente e aprovados, sem falhas (validation/results/referencia_atualizada.xml). Não foram somados aos 80 casos da execução completa anterior. A versão de 33 páginas foi renderizada e conferida visualmente; o quadro comparativo teve a formatação uniformizada. A modalidade adotada é monografia, conforme confirmação da autora.
