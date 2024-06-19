import streamlit as st

from streamlit_extras.stylable_container import stylable_container

from utils.ui_components import menu, custom_button
from utils.resources import init_resources
from utils.streamlit_utils import set_page_config

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Set page_config
set_page_config(page_title="Home")
# initialize resources
init_resources()
# Sidebar Menu
menu()

def generate_response(response):
    for result in response:
        yield result.text

def column1_ui():

    st.markdown("""
    <div style='font-size: 18px; color: #c7ccd1;'>
    Select the following option first:
    </div>
    """, unsafe_allow_html=True)
    st.text("")

    collections = st.session_state.chroma_client.list_collections()
    collection_select = st.selectbox(
        "Collection",
        [col.name for col in collections]
    )

    st.text("")

    model_select = st.selectbox(
        "LLM Model",
        ["GOOGLE AI Studio : gemini-1.5-pro-latest",
         "GOOGLE AI Studio : gemini-1.0-pro-latest",
         "GOOGLE AI Studio : gemini-1.0-pro-001",
         "GOOGLE AI Studio : gemini-1.0-pro",
         "GOOGLE AI Studio : gemini-pro",
         "Vertex AI : gemini-1.0-pro", 
         "Vertex AI : gemini-1.0-pro-001",
         "Vertex AI : gemini-1.0-pro-002",
         "Vertex AI : gemini-1.5-pro-preview-0409"],
         index=0
    )
    # st.text("")

    input_prompt = st.text_area(
        "Question",
        "",
        placeholder="Type your question"
    )

    # st.text("")

    subcol1, subcol2 = st.columns([0.8, 0.2])
    with subcol1:
        st.text("")

    # Button in the first (left) column
    with subcol2:
        submit = custom_button(button_label="Ask")
    return collection_select, model_select, input_prompt, submit

def column3_ui(collection, model, query, submit):

    st.markdown("<span style='font-size: 18px; color: #c7ccd1;'>Answer Section:</span>",
                unsafe_allow_html=True)
    col1, col2 =st.columns([0.06, 0.94])
    with col1:
        st.image('img/billy.png', width=40)
    with col2:
        st.markdown("<span style='font-size:28px;'>. . .</span>", unsafe_allow_html=True)

    if submit:
        st.session_state.llm.setup_qanda_model(model)
        collection = st.session_state.chroma_client.get_collection( name=collection, 
                                                                    embedding_function=st.session_state.llm.embedding_function )
        results = collection.query( query_texts=[query], 
                                    n_results=10,
                                    include=["documents", "metadatas"] )

        sources = "\n".join([ f"{result['url']} \n" for result in results["metadatas"][0]  ])

        response = st.session_state.llm.get_gemini_response( query, results["documents"][0])

        st.write_stream(generate_response(response))
    
        st.write((f"Reference URLs :\n\n{sources}"))

def main():

    # Page Header
    st.title(":violet[Billy] **is here** :rainbow[...]")
    #Ask me anything you want to know about your saved collections.
    st.markdown("""
    <div style='font-size: 30px; color: #4a4e69;'>
    What brings you in today? I'm ready to help you.
    </div>
    """, unsafe_allow_html=True)
    st.text("")
    st.subheader("", divider='rainbow')
    st.text("")

    # Body
    col1, col2, col3 = st.columns([0.4, 0.05, 0.7])
    with col1:
        collection, model, input, submit = column1_ui()

    with col2:
        st.text("")

    with col3:
        column3_ui(collection, model, input, submit)

if __name__ == "__main__":
    main()