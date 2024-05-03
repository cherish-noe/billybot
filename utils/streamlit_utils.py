import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stylable_container import stylable_container

def set_page_config(page_title):
    st.set_page_config(
        page_title=page_title,
        layout="wide"
    )


def add_sidebar_logo():
    add_logo(
        "./img/sidebar-logo.png",
        height=170
    )