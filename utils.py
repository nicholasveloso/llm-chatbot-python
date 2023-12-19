import streamlit as st

def write_message(role, content, save = True):
    """
    Esta é uma função auxiliar que salva uma mensagem no 
    estado da sessão e depois grava uma mensagem na UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)