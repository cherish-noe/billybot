import math
import re
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from utils.streamlit_utils import set_page_config
from utils.ui_components import menu, custom_button
from utils.resources import init_resources

# Set page_config
set_page_config(page_title="My Collections")
# initialize resources
init_resources()
# Sidebar Menu
menu()
session = st.session_state

def remove_url_prefix(url):
    # Regular expression to match http://www. or https://www.
    pattern = re.compile(r'^https?://')
    # Substitute the matched pattern with an empty string
    return pattern.sub('', url)
 
def transform_text(text):
    # Capatialize the first letter of each word
    text = text.title()
    return text



def get_collections_metadatas(collection_names):

    collection_urls = []
    collection_titles = []
    for collection in collection_names:
        collection = session.chroma_client.get_collection( name=collection, 
                                                    embedding_function=session.llm.embedding_function )
        results = collection.get( ids = ["0"],
                                include=[ "metadatas"] )
        if results['metadatas']:
            collection_urls.append(results['metadatas'][0]['url'])
            if "title" in results['metadatas'][0]:
                collection_titles.append(results['metadatas'][0]['title'])
            else:
                collection_titles.append(None)
        else:
            collection_urls.append(None)
            collection_titles.append(None)
    return collection_urls, collection_titles

def show_collection_as_card(col, collection_names, displayed_colls, collection_urls, collection_titles, i, j):
    with col:
        with col.container(border=True, height=348):
            #e4d9ff
            #Collection Header
            subcol1, subcol2, subcol3, subcol4 = st.columns(4)
            with subcol1:
                st.markdown(f'''<span style='font-size: 21px; color: #cbc0d3; font-family: Gill Sans, sans-serif;'>
                            <b>{transform_text(collection_names[displayed_colls])}</b>
                            </span>''', unsafe_allow_html=True)

            with subcol2:
                st.markdown("")
            with subcol3:
                st.markdown("")
            with subcol4:
                with st.popover("", use_container_width=True):
                    st.markdown("Are you sure to delete this collection?")
                    input = st.text_input("Type 'Delete' to delete this.", key=f"input-{i}-{j}")
                    submit = st.button("Delete", key=f"button-{i}-{j}")
                    if submit and input == "Delete":
                        session.chroma_client.delete_collection(collection_names[displayed_colls])
                        st.rerun()
                
            
            # Website iframe
            if collection_urls[displayed_colls]:
                st.components.v1.iframe(collection_urls[displayed_colls])
            else:
                st.image("img/img_not_ava.png")

            # Website Metadata
            if collection_titles[displayed_colls]:
                st.markdown(f"""**{collection_titles[displayed_colls]}**""")
            else:
                st.markdown("**No title is found!**")
            if collection_urls[displayed_colls]:
                st.markdown(f"""
                        <a style='color: grey; text-decoration: none;' href="{collection_urls[displayed_colls]}">{remove_url_prefix(collection_urls[displayed_colls])}</a>
                        """, 
                        unsafe_allow_html=True)
            else:
                st.markdown(f"""
                        <span style='color: grey;'>No link is found!</span>
                        """, 
                        unsafe_allow_html=True)
                # st.markdown("No link is found!")

def show_collections_as_cards(collection_names, num_rows):

    displayed_colls = 0
    collection_urls, collection_titles = get_collections_metadatas(collection_names)

    for i, row in enumerate(range(num_rows)):
        row = st.columns(4, gap="small")
        for j, col in enumerate(row):
            if displayed_colls < len(collection_names):
                show_collection_as_card(col, collection_names, displayed_colls, 
                                        collection_urls, collection_titles, i, j)
                displayed_colls += 1

def main():
    # App Content

    # 'Create' Collection Button
    col1, col2 = st.columns([0.9, 0.115]) 
    with col1:
        st.markdown("")
    with col2:
        submit = custom_button(button_label="**＋ CREATE**")
        if submit:
            st.switch_page("pages/create_collection.py")

    # Title and Description
    st.markdown("""
    <h1 style='text-align: center; color: #f8f4f1;'>My Collections</h1>
    <div style='text-align: center; color: #7f7f7f; font-size: 17px;'>
    Manage your collections: search, view, delete or create new ones - all from here.
    </div>
    """, unsafe_allow_html=True)

    # Search or select existing collection
    col3, col4 = st.columns([0.9, 0.1])
    with col3:
        collection_select = st.multiselect(
        label="Collection Select",
        options=[col.name for col in session.chroma_client.list_collections()],
        key="c_select",
        placeholder="Search or select your collections",
        label_visibility="hidden"
        )

    with col4:
        st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)
        search = st.button("Search", use_container_width=True)
    st.text("")

    if collection_select and search:
        # Collection list
        num_rows = math.ceil(len(collection_select) / 4)
        show_collections_as_cards(collection_select, num_rows)
    else:
        # Collection list
        num_collections = session.chroma_client.count_collections()
        num_rows = math.ceil(num_collections / 4)
        collection_names = [coll.name for coll in session.chroma_client.list_collections()]

        show_collections_as_cards(collection_names, num_rows)

if __name__ == "__main__":
    main()