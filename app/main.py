import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from ui.streamlit_ui import render_page_config, render_database_selection, render_connection_inputs
from database.database_factory import create_connection

def validate_and_connect(db_type, connection_details):
    """
    Validates connection details and attempts to establish a database connection.
    Returns True if successful, False otherwise.
    """
    if not all(connection_details.values()):
        st.error("Please fill in all required connection details.")
        return False
    else:
        try:
            db_connection = create_connection(db_type, **connection_details)
            if db_connection.test_connection():
                st.success("Connection established successfully!")
                return True
            else:
                st.error("Failed to establish a connection. Please check your details.")
                return False
        except Exception as e:
            st.error(f"Connection error: {e}")
            return False
        
def setupLLMChain():
    """
    Initializes and returns a Language Model (LLM) Chain configured for conversation. This setup includes:
    - A PromptTemplate that defines how the chatbot should perceive the conversation context and structure its responses.
    - A ChatOpenAI instance configured with an API key to communicate with OpenAI's language models.
    - A ConversationBufferWindowMemory instance that maintains a sliding window of chat history for contextual awareness.

    The function creates and returns an LLMChain object, which combines these components to facilitate generating responses based on the input question and chat history, ensuring the chatbot behaves as a kind and friendly AI assistant with a sense of humor.
    """
    prompt = PromptTemplate(
        input_variables=["chat_history", "question"],
        template="""You are a very kindl and friendly AI assistant. You are
        currently having a conversation with a human. Answer the questions
        in a kind and friendly tone with some sense of humor.
        
        chat_history: {chat_history},
        Human: {question}
        AI:"""
    )

    llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
    memory = ConversationBufferWindowMemory(memory_key="chat_history")

    return LLMChain(
        llm=llm,
        memory=memory,
        prompt=prompt
    )      

def main():
    """
    Main function to initialize the app and handle the UI and business logic.
    """

    load_dotenv() # Load environment variables from .env file

    llm_chain = setupLLMChain() # Setup LLM chain

    render_page_config() # Render the application configuration

    with st.sidebar:
        
        db_type = {}
        connection_details = {}

        db_type = render_database_selection()
        need_connection_details = db_type != "Select a database" and db_type != "Default (Azure CosmosDB)"

        if need_connection_details:
            connection_details = render_connection_inputs(db_type)
    
        if need_connection_details and st.sidebar.button("Test Connection", key="test_connection"):
            validate_and_connect(db_type, connection_details)

        if st.sidebar.button("Start Chat", key="start_chat"):
            if db_type == "Default (Azure CosmosDB)" or (need_connection_details and all(connection_details.values())):
                successful_connection = validate_and_connect(db_type, connection_details)
                if successful_connection:
                    st.session_state['chat_started'] = True
                    st.experimental_rerun()
                else:
                    st.error("Connection not valid!")
        if st.sidebar.button("End Chat", key="end_chat"):
            st.session_state['chat_started'] = False
            st.session_state['chat_messages'] = []
            st.experimental_rerun()

    # check for messages in session and create if not exists
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello there, I am AI Chatbot Database Assistant"}
        ]

    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input("Say something")

    if user_prompt is not None:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)


    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                ai_response = llm_chain.predict(question=user_prompt)
                st.write(ai_response)
        new_ai_message = {"role": "assistant", "content": ai_response}
        st.session_state.messages.append(new_ai_message)

if __name__ == "__main__":
    main()