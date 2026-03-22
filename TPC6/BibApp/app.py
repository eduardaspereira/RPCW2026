import re
from flask import Flask, render_template, abort
from mquery import exec_query
from datetime import datetime

app = Flask(__name__)

data_hora_local = datetime.now()
data_iso = data_hora_local.strftime('%Y-%m-%dT%H:%M:%S') 

@app.route('/')
@app.route('/livros')
def index():
    q= """
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?livroID ?titulo ?tipoID ?nomeAutor ?pais WHERE {
        ?livro a ?tipo .
        FILTER(?tipo IN (:LivroHistorico, :LivroFiccional, :LivroParadoxal))
        OPTIONAL { ?livro :titulo ?titulo . }
        ?livro :escritoPor/:nome ?nomeAutor .
        ?livro :escritoPor/:paisOrigem ?pais .
        BIND(STRAFTER(STR(?livro), "#") AS ?livroID)
        BIND(STRAFTER(STR(?tipo), "#") AS ?tipoID)
    } ORDER BY ?titulo
    
    """
    res = exec_query(q)
    livros = []
    for livro in res["results"]["bindings"]:
        l = {
            "id": livro["livroID"]["value"],
            "tipo": livro["tipoID"]["value"],
            "autor": livro["nomeAutor"]["value"],
            "pais": livro["pais"]["value"],
        }
        if "titulo" in livro:
                l["titulo"] = livro["titulo"]["value"]
        livros.append(l)
    return render_template("lista.html", livros = livros)


@app.route('/livro/<id_livro>')
def rota_detalhe(id_livro):
    query = f"""
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?titulo ?tipoURI ?nomeAutor ?pais
           (GROUP_CONCAT(DISTINCT ?linha; SEPARATOR=",,") AS ?linhas)
           (GROUP_CONCAT(DISTINCT ?nomeEvento; SEPARATOR="||") AS ?eventosNomes)
           (GROUP_CONCAT(DISTINCT ?descricao; SEPARATOR="||") AS ?eventosDesc)
    WHERE {{
        OPTIONAL {{:{id_livro} :titulo ?titulo .}}
        :{id_livro} a ?tipoURI .   
        FILTER(?tipoURI IN (:LivroHistorico, :LivroFiccional, :LivroParadoxal))
        :{id_livro} :escritoPor/:nome ?nomeAutor .
        :{id_livro} :escritoPor/:paisOrigem ?pais .
        OPTIONAL {{:{id_livro} :existeEm ?linha .}}
        OPTIONAL {{:{id_livro} :refereEvento ?evento .
                   ?evento :designacao ?nomeEvento .
                   ?evento :descricao ?descricao .}}
    }}
    GROUP BY ?titulo ?tipoURI ?nomeAutor ?pais
    """
    res = exec_query(query)
    livro = None
    
    if res and res["results"]["bindings"]:
        row = res["results"]["bindings"][0]
        
        # Processar linhas temporais
        linhas_raw = row.get("linhas", {}).get("value", "")
        linhas = [x for x in linhas_raw.split(",,") if x] if linhas_raw else []
        
        # Processar eventos
        eventos_nomes_raw = row.get("eventosNomes", {}).get("value", "")
        eventos_desc_raw = row.get("eventosDesc", {}).get("value", "")
        
        eventos_nomes = [x for x in eventos_nomes_raw.split("||") if x] if eventos_nomes_raw else []
        eventos_desc = [x for x in eventos_desc_raw.split("||") if x] if eventos_desc_raw else []
        
        eventos = []
        for i, nome in enumerate(eventos_nomes):
            desc = eventos_desc[i] if i < len(eventos_desc) else "N/A"
            eventos.append({"nome": nome, "desc": desc})
        
        # Cores por tipo
        tipo = row.get("tipoURI", {}).get("value", "").split("#")[-1]
        cores = {
            "LivroHistorico": "w3-blue",
            "LivroFiccional": "w3-purple",
            "LivroParadoxal": "w3-red"
        }
        
        livro = {
            "id": id_livro,
            "titulo": row.get("titulo", {}).get("value", "Sem Título"),
            "tipo": tipo,
            "color": cores.get(tipo, "w3-gray"),
            "autor": row.get("nomeAutor", {}).get("value", "Desconhecido"),
            "pais": row.get("pais", {}).get("value", "N/A"),
            "linhas": linhas,
            "eventos": eventos
        }
    
    if not livro:
        abort(404)
    
    return render_template("detalhe.html", l=livro)


@app.route('/linhas')
def rota_linhas():
    query = """
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?linhaID ?linha (COUNT(DISTINCT ?livro) AS ?numLivros)
    WHERE {
        ?livro :existeEm ?linha .
        BIND(STRAFTER(STR(?linha), "#") AS ?linhaID)
    }
    GROUP BY ?linha ?linhaID
    ORDER BY ?linhaID
    """
    res = exec_query(query)
    linhas = []
    
    if res and res["results"]["bindings"]:
        for row in res["results"]["bindings"]:
            linhas.append({
                "id": row.get("linhaID", {}).get("value", ""),
                "numLivros": row.get("numLivros", {}).get("value", "0")
            })
    
    return render_template("linhas.html", linhas=linhas)


@app.route('/linha/<id_linha>')
def rota_linha(id_linha):
    query = f"""
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?linhaID ?tipo
           (GROUP_CONCAT(DISTINCT ?livroID; SEPARATOR=",,") AS ?livrosIDs)
           (GROUP_CONCAT(DISTINCT ?tituloLivro; SEPARATOR=",,") AS ?livrosTitulos)
           (GROUP_CONCAT(DISTINCT ?tipoLivroID; SEPARATOR=",,") AS ?tiposLivros)
    WHERE {{
        :{id_linha} a ?tipo .
        OPTIONAL {{
            ?livro :existeEm :{id_linha} .
            ?livro a ?tipoLivro .
            FILTER(?tipoLivro IN (:LivroHistorico, :LivroFiccional, :LivroParadoxal))
            OPTIONAL {{ ?livro :titulo ?tituloLivro . }}
            BIND(STRAFTER(STR(?livro), "#") AS ?livroID)
            BIND(STRAFTER(STR(?tipoLivro), "#") AS ?tipoLivroID)
        }}
        BIND(STRAFTER(STR(:{id_linha}), "#") AS ?linhaID)
    }}
    GROUP BY ?linhaID ?tipo
    """
    res = exec_query(query)
    linha = None
    
    if res and res["results"]["bindings"]:
        row = res["results"]["bindings"][0]
        
        livros_ids_raw = row.get("livrosIDs", {}).get("value", "")
        livros_titulos_raw = row.get("livrosTitulos", {}).get("value", "")
        tipos_livros_raw = row.get("tiposLivros", {}).get("value", "")
        
        livros_ids = [x for x in livros_ids_raw.split(",,") if x] if livros_ids_raw else []
        livros_titulos = [x for x in livros_titulos_raw.split(",,") if x] if livros_titulos_raw else []
        tipos_livros = [x for x in tipos_livros_raw.split(",,") if x] if tipos_livros_raw else []
        
        livros = []
        for i, livro_id in enumerate(livros_ids):
            titulo = livros_titulos[i] if i < len(livros_titulos) else "N/A"
            tipo_livro = tipos_livros[i] if i < len(tipos_livros) else "N/A"
            livros.append({"id": livro_id, "titulo": titulo, "tipo": tipo_livro})
        
        tipo_linha = row.get("tipo", {}).get("value", "").split("#")[-1]
        
        linha = {
            "id": id_linha,
            "tipo": tipo_linha,
            "livros": livros
        }
    
    if not linha:
        abort(404)
    
    return render_template("linha.html", linha=linha)


@app.route('/eventos')
def rota_eventos():
    q = """
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?eventoID ?designacao ?descricao
           (GROUP_CONCAT(DISTINCT ?livroID; SEPARATOR=",,") AS ?livrosIDs)
           (GROUP_CONCAT(DISTINCT ?tituloLivro; SEPARATOR=",,") AS ?livrosTitulos)
    WHERE {
        ?livro :refereEvento ?evento .
        OPTIONAL { ?evento :designacao ?designacao . }
        OPTIONAL { ?evento :descricao ?descricao . }
        OPTIONAL { ?livro :titulo ?tituloLivro . }
        BIND(STRAFTER(STR(?evento), "#") AS ?eventoID)
        BIND(STRAFTER(STR(?livro), "#") AS ?livroID)
    }
    GROUP BY ?eventoID ?designacao ?descricao
    ORDER BY ?eventoID
    """
    res = exec_query(q)
    eventos = []
    if res:
        for row in res["results"]["bindings"]:
            livros_ids_raw = row.get("livrosIDs", {}).get("value", "")
            livros_titulos_raw = row.get("livrosTitulos", {}).get("value", "")

            livros_ids = [x for x in livros_ids_raw.split(",,") if x] if livros_ids_raw else []
            livros_titulos = [x for x in livros_titulos_raw.split(",,") if x] if livros_titulos_raw else []

            livros = []
            for i, livro_id in enumerate(livros_ids):
                titulo = livros_titulos[i] if i < len(livros_titulos) else "N/A"
                livros.append({"id": livro_id, "titulo": titulo})

            eventos.append({
                "id": row.get("eventoID", {}).get("value", ""),
                "designacao": row.get("designacao", {}).get("value", "N/A"),
                "descricao": row.get("descricao", {}).get("value", "N/A"),
                "livros": livros,
            })

    return render_template("eventos.html", eventos=eventos)


if __name__ == '__main__':
    app.run(debug=True)