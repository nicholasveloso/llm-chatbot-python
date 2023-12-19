import streamlit as st

# Importando o Neo4j Vector Store.
from langchain.vectorstores.neo4j_vector import Neo4jVector

# Importando classe qa_with_sources.
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

# Importando o a classe RetrievalQA.
from langchain.chains import RetrievalQA

# Importando o LLM.
from llm import llm, embeddings

# Chamando o vector index.
neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              # (1)
    url=st.secrets["NEO4J_URI"],             # (2)
    username=st.secrets["NEO4J_USERNAME"],   # (3)
    password=st.secrets["NEO4J_PASSWORD"],   # (4)
    index_name="moviePlots",                 # (5)
    node_label="Movie",                      # (6)
    text_node_property="plot",               # (7)
    embedding_node_property="plotEmbedding", # (8)
    retrieval_query="""
RETURN
    node.plot AS text,
    score,
    {
        title: node.title,
        directors: [ (person)-[:DIRECTED]->(node) | person.name ],
        actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
        tmdbId: node.tmdbId,
        source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
    } AS metadata
"""
)

# Criando umja instância do Retriever.
retriever = neo4jvector.as_retriever()

# Criando a nova cadeia de RetrievalQA.
kg_qa = RetrievalQA.from_chain_type(
    llm,                  # (1)
    chain_type="stuff",   # (2)
    retriever=retriever,  # (3)
)

# Gerando a função com a resposta.
def generate_response(prompt):
    """
    Usando o Vector Search Index do Neo4j para
    aumentar (aprimorar) a resposta do LLM.
    """

    # Handle the response
    response = kg_qa({"question": prompt})

    return response['answer']