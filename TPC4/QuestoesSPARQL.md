# Questões SPARQL

1. Liste todos os livros que existem na linha temporal original (LinhaOriginal)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?livro ?linha
WHERE {
  ?livro :existemEm ?linha .
  ?linha a :LinhaOriginal .
}
ORDER BY ?livro
```

2. Identifique os livros que existem em mais do que uma linha temporal

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT ?livro (COUNT(DISTINCT ?linha) AS ?numLinhas)
WHERE {
  ?livro :existemEm ?linha .
}
GROUP BY ?livro
HAVING (COUNT(DISTINCT ?linha) > 1)
ORDER BY DESC(?numLinhas) ?livro
```

3. Liste todos os livros classificados como LivroParadoxal.

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?livro
WHERE {
  ?livro a :LivroParadoxal .
}
ORDER BY ?livro
```

4. Para cada LivroHistórico, indique os eventos históricos que esse livro refere.

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?livro ?evento
WHERE {
  ?livro a :LivroHistórico ;
         :refereEvento ?evento .
  ?evento a :EventoHistórico .
}
ORDER BY ?livro ?evento
```

5. Identifique livros classificados como LivroHistórico que referem eventos futuros.

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?livro ?evento
WHERE {
  ?livro a :LivroHistórico ;
         :refereEvento ?evento .
  ?evento a :EventoFuturo .
}
ORDER BY ?livro ?evento
```

6. Liste os autores e o número de livros que escreveram, ordenando por número de livros (desc).

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT ?autor (COUNT(DISTINCT ?livro) AS ?numLivros)
WHERE {
  ?livro :sãoEscritosPor ?autor .
}
GROUP BY ?autor
ORDER BY DESC(?numLivros) ?autor
```

7. Identifique os autores que escreveram pelo menos um livro paradoxal.

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?autor
WHERE {
  ?livro a :LivroParadoxal ;
         :sãoEscritosPor ?autor .
}
ORDER BY ?autor
```

8. Liste todos os livros que existem em pelo menos uma linha temporal alternativa (LinhaAlternativa).

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?livro ?linha
WHERE {
  ?livro :existemEm ?linha .
  ?linha a :LinhaAlternativa .
}
ORDER BY ?livro
```

9. Indique todos os bibliotecários e a biblioteca onde trabalham.

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?bibliotecario ?biblioteca
WHERE {
  ?bibliotecario a :Bibliotecário ;
                 :trabalhamEm ?biblioteca .
}
ORDER BY ?bibliotecario
```

10. Liste todos os livros escritos por Cronos e indique em que linhas temporais esses livros existem.

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-32/>

SELECT DISTINCT ?livro ?linha
WHERE {
  ?livro :sãoEscritosPor :Cronos ;
         :existemEm ?linha .
}
ORDER BY ?livro ?linha
```