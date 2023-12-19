# Importando os templates de prompt.
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# A cadeia de QA para criação de código Cypher.
from langchain.chains import GraphCypherQAChain

# Os prompts padrões usados pela cadeia de QA.
from langchain.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT, CYPHER_QA_PROMPT

# Importando LLM e Grafo.
from llm import llm
from graph import graph

# Criar a variável com o template do prompt a ser usado para geração de código Cypher para busca na base de dados.
CYPHER_DEGREE_GENERATION_TEMPLATE = """
ou are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
Convert the user's question based on the schema.
For movie titles that begin with "The", move "the" to the end, For example "The 39 Steps" becomes "39 Steps, The" or "the matrix" becomes "Matrix, The".

If no context is returned, do not attempt to answer the question.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Example Cypher code:

1. How to find how many degrees of separation there are between two people and the path between them:
```
MATCH path = shortestPath(
  (p1:Person {{name: "Actor 1"}})-[:ACTED_IN|DIRECTED*]-(p2:Person {{name: "Actor 2"}})
)
WITH path, p1, p2, relationships(path) AS rels
RETURN
  p1 {{ .name, .born, link:'https://www.themoviedb.org/person/'+ p1.tmdbId }} AS start,
  p2 {{ .name, .born, link:'https://www.themoviedb.org/person/'+ p2.tmdbId }} AS end,
  reduce(output = '', i in range(0, length(path)-1) |
    output + CASE
      WHEN i = 0 THEN
       startNode(rels[i]).name + CASE WHEN type(rels[i]) = 'ACTED_IN' THEN ' played '+ rels[i].role +' in 'ELSE ' directed ' END + endNode(rels[i]).title
       ELSE
         ' with '+ startNode(rels[i]).name + ', who '+ CASE WHEN type(rels[i]) = 'ACTED_IN' THEN 'played '+ rels[i].role +' in '
    ELSE 'directed '
      END + endNode(rels[i]).title
      END
  ) AS pathBetweenPeople
```
Note: Tell the number of degrees of separation at the beggining of your answer.
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Use Neo4j 5 Cypher syntax.  When checking a property is not null, use `IS NOT NULL`.

Question: 
{question}
"""

# Criando o prompt a partir do template.
cypher_prompt = PromptTemplate.from_template(CYPHER_DEGREE_GENERATION_TEMPLATE)

# Gerar a cadeia QA a ser usada pelo agente.
cypher_degree = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    cypher_prompt=cypher_prompt
)

# Gerar respostas
def generate_response(prompt):
    """
    Use o dataset de recomendações de filmes do Neo4j para 
    prover contexto ao LLM para geração de suas respostas.
    """

    # Handle the response
    response = cypher_degree.run(prompt)

    return response