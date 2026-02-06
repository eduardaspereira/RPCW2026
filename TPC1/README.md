# Manifesto do TPC1

## Metainformação
* **Título:** Semana 1
* **Data:** 06-02-2026
* **Autor:**
    * **Id:** PG61516
    * **Nome:** Eduarda Pereira
    * **Foto:** ![Foto do Autor](../assets/foto.jpg)


## Resumo
Este primeiro trabalho prático serviu para consolidar os conceitos fundamentais de ontologias e a sua manipulação programática. Explorou-se a criação de modelos em OWL/Turtle, a tradução de histórias para grafos de conhecimento e a automação da população de ontologias a partir de fontes externas (JSON). 


## Lista de Resultados

### 1. Sistema de Manifesto
* [manifesto/myManifest.json](manifesto/myManifest.json): Ficheiro de metadados do manifesto em formato JSON.
* [manifesto/json2ttl.py](manifesto/json2ttl.py): Conversor de metadados JSON para instâncias ontológicas (TTL).
* [manifesto/manifest.ttl](manifesto/manifest.ttl): Instância ontológica do manifesto. 
* [manifesto/geraReadMe.py](manifesto/geraReadMe.py): Script que gera este ficheiro README.md a partir do TTL.

### 2. Exercício da História (Línguas)
* [linguas/historia.ttl](linguas/historia.ttl): Ontologia que descreve as personagens e competências linguísticas da história do Eduardo.

### 3. Exercício da Lista de Compras
* [listaCompras/json2ttl.py](listaCompras/json2ttl.py): Script Python que converte o dataset de compras para formato RDF.
* [listaCompras/populacao.ttl](listaCompras/populacao.ttl): Instâncias geradas automaticamente a partir do ficheiro JSON de compras. 
* [listaCompras/lista_compras.json](lista_compras.json): Ficheiro de metadados com a lista de compras fornecido no pdf em formato JSON. 


