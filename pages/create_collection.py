import sys
import streamlit as st

from tqdm import tqdm
from utils.apify_utils import scrape_web
from utils.resources import init_resources
from utils.ui_components import custom_button, menu
from utils.streamlit_utils import set_page_config

# Set page_config
set_page_config(page_title="Create Collection")
# initialize resources
init_resources()
session = st.session_state
# Sidebar Menu
menu()

def chunk_large_text(text, size=2200):
    """Yield successive size chunks from text."""
    for start in range(0, len(text), size):
        print(sys.getsizeof(text[start:start + size]))
        yield text[start:start + size]

def create_collection(collection_name, input_url, depth):
    
    with st.spinner("We're scraping content from the provided website. This could take an hour to several hours, depending on the complexity and size of the site. Feel free to grab a coffee or take a nap while you wait!"):
        
        collection = session.chroma_client.get_or_create_collection(name=collection_name, 
                                                                    embedding_function=session.llm.embedding_function,)
        run, apify_client = scrape_web(session.apify_client, input_url, depth)
        
        docs, metadatas, ids = [], [], []
        for i, item in enumerate(apify_client.dataset(run["defaultDatasetId"]).iterate_items()):
            docs.append(item['markdown'])
            metadatas.append({"url" : item['url'], 
                              "title": item['metadata']['title']})
            ids.append(str(i))
            print({"url" : item['url'], "title": item['metadata']['title']})

        for i, doc in enumerate(docs):
            document_size = sys.getsizeof(doc)
            if document_size >= 10000:
                # Document exceeds the size limit, split it into chunks
                chunks = list(chunk_large_text(doc))
                chunk_ids = [f"{ids[i]}_{idx}" for idx, _ in enumerate(chunks)]
                chunk_metas = [{"url": metadatas[i]['url'], "title": metadatas[i]['title']} for _ in chunks]
                print(chunk_ids)
                print(chunk_metas)
                for chunk_id, chunk, chunk_meta in zip(chunk_ids, chunks, chunk_metas):
                    collection.add(ids=[chunk_id], documents=[chunk], metadatas=[chunk_meta])
                # print(f"Added document {ids[i]} in {len(chunks)} chunks due to size {document_size} bytes.")
            else:
                # Document within size limit, add as is
                collection.add(ids=[ids[i]], documents=[doc], metadatas=[metadatas[i]])
                # print(f"Added document {ids[i]} with size {document_size} bytes.")

    st.success(f'{collection_name} is successfully created!')

def main():

    col1, col2, col3 = st.columns([0.4, 0.4, 0.1])

    with col1:
        # Add logo within the page body
        st.markdown("")
        st.image("img/billybot.gif")

    with col2:
        st.markdown("""
        <h1 style='text-align: center; color: #f8f4f1;'>Create Collection</h1>
        <div style='text-align: center; color: #adb5bd; font-size: 17px'>
        Turn a website's content into your own collection - just paste the website URL.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("", divider="grey")
        st.markdown("")

        collection_name = st.text_input('''**:violet[Collection Name *]**''',  "", placeholder="space is not allowed")
        input_url = st.text_input( '''**:violet[Website Url *]**''', "", placeholder="https://www.billybot.com")
        depth = st.text_input('''**:violet[Crawling Depth *]**  
                              :grey[(start URL = 0, its links = 1, and so on.)]''',value=20, placeholder="20",
                            help="The maximum number of links starting from the start URL that the crawler will recursively follow. The start URLs have depth 0, the pages linked directly from the start URLs have depth 1, and so on. Deafult value is 20.")
  
        #:grey[(only start URL = 0, its links = 1, and so on. For more details: [link](https://apify.com/apify/website-content-crawler/input-schema).)]'''
        st.markdown("")

        subcol1, subcol2 = st.columns([0.8, 0.2])
        with subcol1:
            st.markdown("")

        # Button in the first (left) column
        with subcol2:
            submit = custom_button(button_label="Create")
        if submit:
            create_collection(collection_name, input_url, depth)

    with col3:
        st.markdown("")


if __name__ == "__main__":
    main()