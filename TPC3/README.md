# Manifesto do TPC3

## Metainformação
* **Título:** Semana 3
* **Data:** 02-03-2026
* **Autor:**
    * **Id:** PG61516
    * **Nome:** Eduarda Pereira
    * **Foto:** ![Foto do Autor](../assets/foto.jpg)

## Resumo
Este terceiro trabalho prático consiste no desenvolvimento de uma ontologia em OWL (Web Ontology Language) para modelar o ecossistema invulgar de um restaurante fictício chamado "O Polvo Filosófico", situado na vila de Ontolândia. O objetivo principal é criar um modelo capaz de lidar com agentes de naturezas distintas — humanos, animais e máquinas — e aplicar regras de negócio que desafiam a lógica convencional.

## Lista de Resultados
* [polvo.ttl](polvo.ttl): Instância ontológica de *O Restaurante “O Polvo Filosófico”*. 

## Respostas 
1. Alterações
- **Alteração:** As classes :Funcionário e :Cliente foram definidas como subclasses diretas de :Agente.  
    **Justificação:** O domínio apresenta agentes não-humanos, como o polvo Aristóteles (gestor) e o RoboCozinheiro (máquina/cozinheiro).  

- **Alteração:** Foi criada a classe :Gestor (subclasse de :Funcionário) atribuída especificamente ao indivíduo :Aristoteles.  
    **Justificação:** Reflete a semântica do domínio onde Aristóteles desempenha funções de gestão, permitindo a organização dos tipos de funcionários.

- **Alteração:** A classe :PratoVegano foi definida como uma owl:equivalentClass baseada na ausência de ingredientes de origem animal.  
    **Justificação:** Assim, o reasoner consegue inferir que qualquer prato sem ingredientes de origem animal é, por definição, um :PratoVegano.


2. Quem foram os clientes?  
O único cliente foi o gato Schrödinger.

3. Que pratos serve o restaurante?  
Servem-se pratos veganos, carnívoros e ontologicamente ambíguos. 

4. Quais os ingredientes necessários á confeção dos pratos?   
Os ingredientes podem ser de origem animal ou polvo.

5. Há funcionários que sejam também clientes?  
Sim, como é o caso do Schrödinger.