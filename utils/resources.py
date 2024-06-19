import os
import chromadb
import streamlit as st

from dotenv import load_dotenv
from apify_client import ApifyClient

from utils.llm import LLM

def init_resources():
    load_dotenv()

    # add to session state dict
    if "llm" not in st.session_state:
        llm = LLM()
        st.session_state['llm'] = llm
    if "apify_client" not in st.session_state:
        apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
        st.session_state['apify_client'] = apify_client
    if "chroma_client" not in st.session_state:
        chroma_client = chromadb.PersistentClient( path="chroma_storage" )
        st.session_state['chroma_client'] = chroma_client
