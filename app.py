#Importing all the librairies
import streamlit as st
import requests
import os
from scrape import extract_text
from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import ServiceContext
from pinecone import Pinecone, ServerlessSpec
import pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding


def create_index_custom(index_name:str,pc):
    # pc = Pinecone(api_key=pinecone_api_key)
    if index_name not in pc.list_indexes().names():
        pc.create_index(
        name=index_name,
        dimension=1536, # Replace with your model dimensions
        metric="cosine", # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
        )



#Setting up all the api keys from .env file 
google_api_key=os.getenv("GOOGLE_API_KEY")
pinecone_api_key=os.getenv("PINE_CONE_API_KEY")
openai_api_key=os.getenv("OPENAI_API_KEY")
if "index_created" not in st.session_state:
    st.session_state.index_created = False

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

#Splitted text is stored here 
nodes = []
#streamlit user interface is started
user_input=st.text_input("Enter Website link?", st.session_state.user_input)

#Making api call to the WebUrl and extracting text from the link
if user_input and not st.session_state.index_created:
    html_text = requests.get(user_input).text
    extracted_text = extract_text(html_text)



    text_parser = SentenceSplitter(chunk_size=550,chunk_overlap=200)

    text_chunks = text_parser.split_text(extracted_text)
    print(text_chunks)
    print(len(text_chunks))
    
    for idx, text_chunk in enumerate(text_chunks):
        node = TextNode(
            text=text_chunk,
        )

        nodes.append(node)
    
    # print a sample node
    print(nodes[0].get_content(metadata_mode="all"))
    embed_model = OpenAIEmbedding()

    #Creating embedding for eact chunck
    for node in nodes:
        node_embedding = embed_model.get_text_embedding(node.get_content(metadata_mode="all"))
        node.embedding = node_embedding
    
    pc =  Pinecone(api_key=pinecone_api_key)
    index_name="demo-index-6"

    #creating pinecone vector index 

    create_index_custom(index_name,pc)
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    #adding nodes to the pinecone vector index
    if pinecone_index.describe_index_stats()['total_vector_count'] != len(text_chunks):

        vector_store.add(nodes)
    st.session_state.index_created = True
    st.session_state.vector_store = vector_store

    # Streamlit user interface for querying
if st.session_state.index_created and st.session_state.vector_store:
        #Initialising the gemini Model
    query_input = st.text_input("Enter your query:")
    if query_input:
        # # model = Gemini(models='gemini-pro',api_key=google_api_key)
        # Settings.llm = model
         
        # gemini_embed_model=GeminiEmbedding(model_name="models/embedding-001")
        # Settings.embed_model =  gemini_embed_model

        vector_store = st.session_state.vector_store
        #loading the created index from pine cone
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        query_engine = index.as_query_engine()
        print(query_input)
        response = query_engine.query(query_input)
        st.success(str(response.response))





