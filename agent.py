# Importando a classe Tool.
from langchain.tools import Tool

# Importando métodos necessários para os agentes.
from langchain.agents import initialize_agent, AgentType
from langchain.agents import ConversationalChatAgent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Incluíndo o LLM gerado no arquivo llm.py.
from llm import llm

# Usando a cadeias definida como ferramenta para o agente em vector.py.
from tools.vector import kg_qa
# Usando a cadeias definida como ferramenta para o agente em cypher.py.
from tools.cypher import cypher_qa
# Usando a cadeias definida como ferramenta para o agente em degree.py.
from tools.degree import cypher_degree

# Definindo as ferramentas.
tools = [
    # Ferramenta para fazer a buscas do número de graus de separação e caminho entre duas pessoas.
        Tool.from_function(
        name="Cypher Degrees of Separation and shortest movie path",
        description="Provide information about how many degrees of separation there are between two people via a movie they share in common using Cypher, and try to find the shortest path between them.",
        func = cypher_degree,
    ),
    # Ferramenta para fazer busca na nase de dados de grafos usando Cypher.
        Tool.from_function(
        name="Cypher QA",
        description="Provide information about movies questions using Cypher. Also.",
        func = cypher_qa,
    ),
    # Ferramenta para fazer busca semântica usando o Vector Index e retornar informações sobre enredo dos filmes.
    Tool.from_function(
        name="Vector Search Index",  # (1)
        description="Provides information about movie plots using Vector Search", # (2)
        func = kg_qa, # (3)
    )
]

# Inicializando a memória.
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
)

# O prompt limitando o escopo do agente.abs
SYSTEM_MESSAGE = """
You are a movie expert providing information about movies.
Be as helpful as possible and return as much information as possible.
Do not answer any questions that do not relate to movies, actors or directors.

Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.
"""

# Inicializando o agente.
agent = initialize_agent(
    tools,
    llm,
    memory=memory,
    verbose=True,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    agent_kwargs={"system_message": SYSTEM_MESSAGE}
)

# Criando a função para gerar resposta.
def generate_response(prompt):
    """
    Cria um handler que chama o agente conversacional 
    e retorna a resposta a ser renderizada na UI
    """

    response = agent(prompt)

    return response['output']