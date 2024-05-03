import os
import vertexai
import google.generativeai as genai

from vertexai.preview.generative_models import GenerativeModel
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

from chromadb import EmbeddingFunction, Embeddings


class CustomVertexAIEmbeddings(EmbeddingFunction):
    def __init__(self, embedder) -> None:
        self.embedder = embedder

    def __call__(self, input) -> Embeddings:
        embedded_texts = self.embedder.embed_documents(texts=input)
        return embedded_texts

class Prompt:
    def _build_prompt(self, query, context) -> str:
        """
        Builds a prompt for the LLM. 

        Args:
        query (str): The original query.
        context (List[str]): The context of the query, returned by embedding search.

        Returns:
        A prompt for the LLM (str).
        """

        base_prompt = {
            "content": "I am going to ask you a question, which I would like you to answer"
            " based only on the provided context, and not any other information."
            " If there is not enough information in the context to answer the question,"
            ' say "I am not sure", then try to make a guess.'
            " Break your answer up into nicely readable paragraphs.",
        }
        user_prompt = {
            "content": f" The question is '{query}'. Here is all the context you have:"
            f'{(" ").join(context)}',
        }
        # combine the prompts to output a single prompt string
        system = f"{base_prompt['content']} {user_prompt['content']}"

        return system

class LLM(Prompt):
    def __init__(self) -> None:
        super().__init__()
        self.use_google_ai_studio = False
        self.use_vertex = False
        self._setup_ai_platforms()
        self._setup_embedding_function()
    
    def _setup_ai_platforms(self):

        if os.getenv("GOOGLE_AI_STUDIO_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))
            self.use_google_ai_studio = True
        if os.getenv("PROJECT_ID") and os.getenv("LOCATION"):
            vertexai.init( project=os.getenv("PROJECT_ID"), 
                           location=os.getenv("LOCATION"))
            self.use_vertex = True

    def _setup_embedding_function(self):

        if self.use_google_ai_studio:
            self.embedding_function = GoogleGenerativeAiEmbeddingFunction(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"),
                                                                          task_type="RETRIEVAL_QUERY")
        elif self.use_vertex:
            self.embedding_function = CustomVertexAIEmbeddings(VertexAIEmbeddings(model_name="textembedding-gecko@003"))

    def setup_qanda_model(self, model_text):
        
        ai_type = model_text.split(" : ")[0]
        model_str = model_text.split(" : ")[1]
        if ai_type == "Vertex AI" and self.use_vertex: 
            self.model = GenerativeModel(model_str)
        elif ai_type == "GOOGLE AI Studio" and self.use_google_ai_studio:
            self.model = genai.GenerativeModel(model_str)
        else:
            print(ai_type, self.use_vertex, self.use_google_ai_studio)
            print("Setup the ai platform by adding the API keys in the .env file.")


    def get_gemini_response(self, query, context) -> str:
        """
        Queries the Gemini API to get a response to the question.

        Args:
        query (str): The original query.
        context (List[str]): The context of the query, returned by embedding search.

        Returns:
        A response to the question.
        """
        return self.model.generate_content(self._build_prompt(query, context), stream=True)

        # response = self.model.generate_content(self._build_prompt(query, context), stream=True)

        # return response.text