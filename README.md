# BillyBot - Your AI Assistant

Tired of confusing official documentation searches? Our AI assistant, Billy, helps you find the answers you need instantly. Our solution curates your official documentation or any website into a searchable collection. You just need to spend some time for changing your website into a collection. Ask natural language questions and get the information you need directly - no more endless link clicking.

You can check the demo video [here.](https://youtu.be/e5U9rEFco44?si=rddFY35bgMQxadAE)


## Installation 

### Conda Installation (Recommended)

#### 1. Setup up credentials

1. Install GCloud CLI and check this [link](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev) for setting up Vertext AI.
(You need to have Google Cloud account and setup a project to use Vertex AI. If you don't, you can go to next step.)
2.  Get API Key for [Google AI Studio](https://aistudio.google.com/app/apikey). Google AI Studio is more straightforward and easy to use than Vertex AI above. 
3. Get the API Key token from [Apify](https://apify.com/) for scraping websites. Create an account and get the API key from [here](https://console.apify.com/account/integrations)
4. Create a .env file and add the credentials and API to it. Check the [.env.example](.env.example) for example. Below is the example content inside the .env file. 

```bash
# Gemini
GOOGLE_AI_STUDIO_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
# vertex ai
PROJECT_ID=xxx-xxxx-xxx
LOCATION=us-central1
# Apify
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxx
```

#### 2. Create Conda environment. 
```bash
conda create --name billy-bot python=3.10
```

#### 3. Install required packages.
```bash
pip install -r requirements.txt --no-cache-dir
```

#### 4. Download the sample collections. 

You can download our sample collection, [chroma_storage.tar.gz](https://github.com/cherish-noe/billybot/releases/download/v0.1/chroma_storage.tar.gz)

```bash
cd billybot
wget https://github.com/cherish-noe/billybot/releases/download/v0.1/chroma_storage.tar.gz
```
Extract it.
```bash
tar xzvf chroma_storage.tar.gz
```

#### 5. Run the app. 
```bash
streamlit run app.py
```


### Docker Installation (Still in development)

Docker Installation only supports Google AI Studio based models at the moment. 

#### 1. Build docker image
```bash
./docker/build_docker.sh --build
```

#### 2. Run our app inside docker container
```bash
docker run -it --rm -p 8511:8511 --name billy-bot billy-bot
```

## Tech Stacks and Architecture

1. Vertex AI
2. Google AI Studio
3. Apify
4. ChromaDB
5. Streamlit

<img src="img/architecture.png" alt="architecture" style="width: 80%; max-width: 1000px;"/>
