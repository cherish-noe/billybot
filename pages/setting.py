import os
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from utils.streamlit_utils import set_page_config
from utils.ui_components import menu, custom_button
from utils.resources import init_resources

# Set page_config
set_page_config(page_title="Setting")
# initialize resources
init_resources()
# Sidebar Menu
menu()
session = st.session_state

def google_ai_studio_api_key_input():
    with st.container(border= True):
        google_ai_studio_api_key = st.text_input(label='Your Google AI Studio API Key')
    return google_ai_studio_api_key

def vertex_ai_inputs():
    with st.container(border= True):
        st.write("Install GCP CLI in your machine and authenticate using this [link](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev).")
        project_ID = st.text_input(label='Your Google Cloud Project ID')
        region = st.text_input(label='Your Google Cloud Project Location', value="us-central1")
    return project_ID, region

def all_platforms_inputs():
    google_ai_studio_api_key = google_ai_studio_api_key_input()
    project_ID, region = vertex_ai_inputs()
    return google_ai_studio_api_key, project_ID, region

def main():

    project_ID, region, google_ai_studio_api_key, apify_api_key = None, None, None, None
    if os.path.exists(".env"):
        st.info("***I found a .env file with credentials under your project directory. Adding credentials here will overwrite your existing .env file.***", icon="ℹ️")
    
    st.subheader("Set AI Platform Credentials")
    ai_type = st.selectbox('Select the AI Platform to use', ('Google AI Studio', 'Vertex AI', 'Both'), index=0)
    
    if ai_type == "Google AI Studio":
        google_ai_studio_api_key = google_ai_studio_api_key_input()
    elif ai_type == "Vertex AI":
        project_ID, region = vertex_ai_inputs()

    elif ai_type == "Both":
        google_ai_studio_api_key, project_ID, region = all_platforms_inputs()
    
    st.divider()
    st.subheader("Set Apify Credentials")

    with st.container(border=True):
        apify_api_key = st.text_input(label='Your Apify API Key')

    agree = st.checkbox('I acknowledge that adding these values will overwrite the existing credentials.')
    if agree:
        submit = st.button('Submit Credentials', key='set-ai-platform-creds')
        if submit:
            with open('.env', 'w') as file:
                if google_ai_studio_api_key:
                    file.write(f"GOOGLE_AI_STUDIO_API_KEY={google_ai_studio_api_key}\n")
                if project_ID and region:
                    file.write(f"PROJECT_ID={project_ID}\n")
                    file.write(f"LOCATION={region}\n")
                if apify_api_key:
                    file.write(f"APIFY_API_TOKEN={apify_api_key}\n")
                st.success("Credentials saved successfully.")
    else:
        submit = st.button('Submit Credentials', key='set-ai-platform-creds', disabled=True)




if __name__ == "__main__":
    main()