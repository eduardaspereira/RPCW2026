# TPC5 

## Metainformação
* **Título:** Semana 5
* **Autor:**
    * **Id:** PG61516
    * **Nome:** Eduarda Pereira

## Resumo
Aplicação web para consultar a ontologia RDF da biblioteca "Entre Ontem e Amanhã" para navegação de livros, visualização de detalhes e exploração de eventos, utilizando queries SPARQL.


### Estrutura de Ficheiros

#### **BibApp/app.py**
Aplicação Flask com 3 rotas principais:
- `/livros` - Listagem de todos os livros com título, tipo, autor e país
- `/livro/<id_livro>` - Página de detalhe com informações completas, linhas temporais e eventos referenciados
- `/eventos` - Listagem de eventos com descrição e livros relacionados

#### **BibApp/mquery.py**
Módulo auxiliar que executa queries SPARQL no repositório GraphDB. 

#### **BibApp/templates/layout.html**
Template base com navegação superior (links para Catálogo e Eventos) e rodapé. Utiliza W3.CSS para estilo.

#### **BibApp/templates/lista.html**
Página de catálogo de livros em formato tabela com hiperlinks para detalhes de cada livro.

#### **BibApp/templates/detalhe.html**
Página de detalhe de livro mostrando:
- Informações básicas (título, tipo, autor, país)
- Linhas temporais associadas
- Eventos referenciados com descrição

#### **BibApp/templates/eventos.html**
Página de eventos com lista de todos os eventos e respetivos livros que os referem.


