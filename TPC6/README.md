# TPC6 

## Metainformação
* **Título:** Semana 6 
* **Autor:**
    * **Id:** PG61516
    * **Nome:** Eduarda Pereira

## Resumo
Aplicação web melhorada para consultar a ontologia RDF da biblioteca "Entre Ontem e Amanhã". Além da navegação de livros e eventos, agora inclui exploração de linhas temporais com navegação entre entidades relacionadas.

### Estrutura de Ficheiros

### Backend
[app.py](BibApp/app.py)
- `/livros` - Lista todos os livros
- `/livro/<id>` - Detalhe de um livro
- `/linhas`  - Lista linhas temporais
- `/linha/<id>`  - Detalhe de uma linha temporal
- `/eventos` - Lista eventos

### Templates
[layout.html](BibApp/templates/layout.html) - Template base 

[lista.html](BibApp/templates/lista.html) - Catálogo de livros

[detalhe.html](BibApp/templates/detalhe.html) - Detalhe do livro com links para linhas temporais

[linhas.html](BibApp/templates/linhas.html)- Tabela de linhas temporais com ID e número de livros

[linha.html](BibApp/templates/linha.html)- Detalhe de linha temporal mostrando livros que nela existem

[eventos.html](BibApp/templates/eventos.html) - Lista de eventos com livros relacionados



