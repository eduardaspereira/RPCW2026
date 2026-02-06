from rdflib import Graph, Namespace

g = Graph()
g.parse("manifesto/manifest.ttl", format="turtle", encoding="utf-8")

DNS = Namespace("http://rpcw.di.uminho.pt/2026/manifesto#")

query = """
SELECT ?titulo ?data ?nome ?id WHERE {
    ?tpc a :TPC ;
         :titulo ?titulo ;
         :data ?data ;
         :temAutor ?autor .
    ?autor :temNome ?nome ;
           :temId ?id .
}
"""

results = g.query(query, initNs={"": DNS})

for row in results:
    readme_content = f"""# Manifesto do TPC1

## Metainformação
* **Título:** {row.titulo}
* **Data:** {row.data}
* **Autor:**
    * **Id:** {row.id}
    * **Nome:** {row.nome}
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


"""

with open("../README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)