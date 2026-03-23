import csv
import json
import re
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, OWL, RDFS, XSD

# 1. Configuração de Namespaces
DNS = Namespace("http://www.example.org/disease-ontology#")
g = Graph()

# Carregar a ontologia base
g.parse("medical.ttl", format="turtle")

def clean_id(text):
    """Transforma nomes em IDs válidos para URIs"""
    if not text: return None
    # Remove caracteres especiais e substitui espaços por underscores
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().replace(" ", "_")

# PASSO 1, 2 e 3: Disease_Symptom.csv 
with open('Disease_Syntoms.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # Saltar cabeçalho
    for row in reader:
        disease_name = row[0].strip()
        disease_id = clean_id(disease_name)
        if not disease_id: continue
        
        disease_uri = DNS[disease_id]
        g.add((disease_uri, RDF.type, DNS.Disease))
        
        # Sintomas (colunas 1 em diante)
        for s_name in row[1:]:
            s_name = s_name.strip()
            if s_name:
                s_id = clean_id(s_name)
                s_uri = DNS[s_id]
                g.add((s_uri, RDF.type, DNS.Symptom))
                g.add((disease_uri, DNS.hasSymptom, s_uri))

# PASSO 4: Disease_Description.csv 
description_prop = DNS.description
g.add((description_prop, RDF.type, OWL.DatatypeProperty))
g.add((description_prop, RDFS.domain, DNS.Disease))
g.add((description_prop, RDFS.range, XSD.string))

with open('Disease_Description.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 2:
            d_id = clean_id(row[0])
            desc = row[1].strip()
            if d_id:
                g.add((DNS[d_id], description_prop, Literal(desc)))

# PASSO 5: Gravar med_doencas.ttl
g.serialize(destination="med_doencas.ttl", format="turtle")
print("Ficheiro med_doencas.ttl gerado.")

# PASSO 6 e 7: Disease_Treatment.csv  
with open('Disease_Treatment.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        d_id = clean_id(row[0])
        if not d_id: continue
        
        # Tratamentos/Precauções 
        for t_name in row[1:]:
            t_name = t_name.strip()
            if t_name:
                t_id = clean_id(t_name)
                t_uri = DNS[t_id]
                g.add((t_uri, RDF.type, DNS.Treatment))
                g.add((DNS[d_id], DNS.hasTreatment, t_uri))

# PASSO 8: Gravar med_tratamentos.ttl
g.serialize(destination="med_tratamentos.ttl", format="turtle")
print("Ficheiro med_tratamentos.ttl gerado.")

# --- PASSO 9: doentes.json ---
with open('doentes.json', mode='r', encoding='utf-8') as f:
    doentes = json.load(f)
    for i, doente in enumerate(doentes):
        nome = doente['nome']
        # Criar ID único baseado no nome ou índice
        p_id = f"Patient_{clean_id(nome)}_{i}"
        p_uri = DNS[p_id]
        
        g.add((p_uri, RDF.type, DNS.Patient))
        g.add((p_uri, DNS.name, Literal(nome))) 
        
        for s_name in doente['sintomas']:
            s_id = clean_id(s_name)
            g.add((p_uri, DNS.exhibitsSymptom, DNS[s_id]))

# PASSO 10: Gravar versão final
g.serialize(destination="med_doentes.ttl", format="turtle")
print("Ficheiro med_doentes.ttl gerado.")