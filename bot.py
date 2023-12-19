import streamlit as st
from utils import write_message
from agent import generate_response


# Cofigurando a página
st.set_page_config("Ebert, a movie expert to call your own!", page_icon=":movie_camera:")

# Configurando o estado da sessão.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the GraphAcademy Chatbot!  How can I help you?"},
    ]


# Submetendo a função manipulador (Handler Function).
def handle_submit(message):
    # Manipulando a resposta.
    with st.spinner('Thinking...'):

        response = generate_response(message)
        write_message('assistant', response)


# Criar a interface do Chat.
with st.container():
    # Mostrar a mensagem mensagem armazenada no estado da sessão.
    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)

    # Lidando com qualquer entrada do usuário.
    if prompt := st.chat_input("What is up?"):
        # Exibir mensagem do usuário no contêiner de mensagens de bate-papo. 
        write_message('user', prompt)

        # Gerar uma resposta.
        handle_submit(prompt)
