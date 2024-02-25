import streamlit as st

def render_page_config():
    """
    Configures the Streamlit page settings, including title, icon, and layout, 
    and adds a credit section to the sidebar.
    """
    st.set_page_config(
        page_title="AI Chat Database",
        page_icon="🤖",
        layout="wide"
    )

    st.title("AI Chatbot Database")
    st.write("This tool allows you to query different types of databases using natural language. Select the type of database you wish to query and enter the required connection details.")

    st.sidebar.markdown("""
    ---
    Made with 🤖 by [Vito Verrastro](https://github.com/vverrastro)""")

def render_database_selection(disabled=False):
    db_options = ["Select a database", "Default (Azure CosmosDB)", "Azure CosmosDB"]
    selected_db = st.selectbox("Select the type of database:", db_options, index=0, disabled=disabled)
    return selected_db

def render_connection_inputs(db_type):
    """
    Display input fields for database connection details based on the selected database type.
    Returns a dictionary with the connection details.
    """
    st.subheader("Dettagli Connessione Database")
    if "Azure CosmosDB" in db_type:
        uri = st.sidebar.text_input("URI del Database")
        database_name = st.sidebar.text_input("Nome Database")
        container_name = st.sidebar.text_input("Nome Container")
        primary_key = st.sidebar.text_input("Primary Key")
        return {"uri": uri, "database_name": database_name, "container_name": container_name, "primary_key": primary_key}
    """ elif "MySQL" in db_type or "PostgreSQL" in db_type:
        hostname = st.text_input("Hostname")
        port = st.text_input("Porta", "3306" if db_type == "MySQL" else "5432")
        database_name = st.text_input("Nome Database")
        user = st.text_input("Utente")
        password = st.text_input("Password", type="password")
        return {"hostname": hostname, "port": port, "database_name": database_name, "user": user, "password": password} """