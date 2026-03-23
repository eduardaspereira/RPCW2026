# PR 

## Metainformação
* **Título:** Semana 7
* **Data:** 28-03-2026
* **Autor:**
    * **Id:** PG61516
    * **Nome:** Eduarda Pereira
    * **Foto:** ![Foto do Autor](../assets/foto.jpg)


## Objetivo
Este trabalho consiste em responder a um conjunto de perguntas sobre a ontologia médica e construir queries SPARQL para análise e diagnóstico de doentes.

## O que foi feito
1. Foi validado o modelo RDF da ontologia com as classes `:Disease`, `:Patient`, `:Symptom` e `:Treatment`.
2. Foram criadas queries SPARQL para responder às perguntas pedidas.
3. Foi criada uma query `CONSTRUCT` para inferir diagnósticos (`:hasDisease`) a partir dos sintomas observados em cada doente.
4. Foi criada a query `INSERT` para materializar os diagnósticos inferidos na ontologia.
5. Foram criadas queries de distribuição e agregação para apoiar análise estatística dos dados.

## Ficheiros usados
1. `med_doentes.ttl` como dataset principal, por conter doenças, sintomas, tratamentos e doentes.
2. `sparql.txt` com todas as queries e respostas pedidas no enunciado.

## Explicação do script (`json2ttl.py`)
O script `json2ttl.py` constrói a ontologia final em Turtle a partir de ficheiros CSV/JSON e de uma ontologia base.

### O que recebe (input)
1. `medical.ttl`: ontologia base (classes e propriedades iniciais).
2. `Disease_Syntoms.csv`: doença + lista de sintomas.
3. `Disease_Description.csv`: doença + descrição textual.
4. `Disease_Treatment.csv`: doença + lista de tratamentos/precauções.
5. `doentes.json`: lista de doentes com nome e sintomas.

### O que faz (transformação)
1. Carrega `medical.ttl` para um grafo RDF (`rdflib.Graph`).
2. Normaliza nomes para IDs URI com `clean_id`:
	remove pontuação/caracteres especiais e substitui espaços por `_`.
3. Lê `Disease_Syntoms.csv` e cria triplos:
	`:doenca rdf:type :Disease`, `:sintoma rdf:type :Symptom`, `:doenca :hasSymptom :sintoma`.
4. Define a propriedade `:description` (datatype property) e adiciona descrições das doenças a partir de `Disease_Description.csv`.
5. Lê `Disease_Treatment.csv` e cria triplos:
	`:tratamento rdf:type :Treatment` e `:doenca :hasTreatment :tratamento`.
6. Lê `doentes.json` e cria doentes com ID único (`Patient_<nome>_<indice>`), adicionando:
	`:patient rdf:type :Patient`, `:patient :name "..."` e `:patient :exhibitsSymptom :sintoma`.

### Output
1. `med_doencas.ttl`: com os sintomas e descrições de doenças.
2. `med_tratamentos.ttl`: com os tratamentos.
3. `med_doentes.ttl`: versão final com os doentes.

## Critério de diagnóstico usado
Um doente `?patient` é associado a uma doença `?disease` se todos os sintomas observados no doente estiverem presentes no conjunto de sintomas da doença.

Implementação SPARQL do critério:
1. Selecionar pares `(?patient, ?disease)`.
2. Rejeitar pares onde exista algum sintoma do doente que não exista na doença.
3. Construir ou inserir o triplo `?patient :hasDisease ?disease`.

## Como replicar 
1. Abrir GraphDB Workbench.
2. Criar um repositório vazio.
3. Importar o ficheiro `med_doentes.ttl`.
4. Abrir o separador SPARQL.
5. Executar, por ordem, as queries do ficheiro `sparql.txt`.
