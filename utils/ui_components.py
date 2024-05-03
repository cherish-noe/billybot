import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def menu():
    st.sidebar.image("img/sidebar-logo.png")
    st.sidebar.page_link("app.py", label=":violet[＋ &nbsp; **NEW CHAT**]")
    st.sidebar.markdown("""
                        <div style='font-size: 18px; color: #6c757d; margin-top: 7px; margin-bottom:-25px;'>
                            &nbsp; Collection
                        </div>
                        """,
                        unsafe_allow_html=True)
    st.sidebar.text("")
    st.sidebar.page_link("pages/create_collection.py", label=":grey[✚] &nbsp; Create Collection")
    st.sidebar.page_link("pages/my_collections.py", label=":grey[⌘] &nbsp; My Collections")
    st.sidebar.markdown("""
                        <div style='font-size: 18px; color: #6c757d; margin-top: 7px; margin-bottom:-25px;'>
                            &nbsp; Setting
                        </div>
                        """,
                        unsafe_allow_html=True)
    st.sidebar.text("")
    st.sidebar.page_link("pages/setting.py", label=":violet[⚙️] &nbsp; API Configuration")

def custom_button(button_label=None):
    with stylable_container(
                key="collection_create",
                css_styles="""
                    button {
                        background-color: #7251b5;
                        color: white;
                        border-radius: 10px;
                    }
                """,
        ):
        submit = st.button(button_label, use_container_width=True)
    return submit
