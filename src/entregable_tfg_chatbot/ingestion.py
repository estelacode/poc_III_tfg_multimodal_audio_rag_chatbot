from typing import List
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.indices.multi_modal.base import MultiModalVectorStoreIndex
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.embeddings.clip import ClipEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import ImageDocument, Document
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from llama_index.embeddings.nomic import NomicEmbedding
from llama_index.core import StorageContext, load_index_from_storage
import chromadb
from dotenv import load_dotenv
import os 


_ = load_dotenv()

def load_documents(txt_image_dir:str):
    """Load the context images and text into ImageDocument and Documents"""
    # context images
    documents = SimpleDirectoryReader(txt_image_dir).load_data()

    return documents


def create_multimodal_index(documents:List, persist_dir: str)->MultiModalVectorStoreIndex:
    """Create a multimodal index from a list of documents"""
    # Create  embedding function
    embedding_function = OpenCLIPEmbeddingFunction()
    # Create image loader
    image_loader = ImageLoader()
    # Create text and image embed model
    image_embed_model = ClipEmbedding()
    
    #text_embed_model = CohereEmbedding(api_key=os.getenv('COHERE_API_KEY'))

    text_embed_model = NomicEmbedding(api_key=os.getenv('NOMIC_API_KEY'), model_name="nomic-embed-text-v1.5", dimensionality=512)
    # create client and a new collection
    chroma_client = chromadb.PersistentClient(path=persist_dir)

    # Create text collection
    txt_collection = chroma_client.get_or_create_collection(name="text_collection", metadata={"hnsw:space": "cosine"}, embedding_function=embedding_function)

    # create img collection
    img_collection = chroma_client.get_or_create_collection(name="images_collection", metadata={"hnsw:space": "cosine"}, embedding_function=embedding_function, data_loader=image_loader)

    # Create text vector store 
    text_store = ChromaVectorStore(chroma_collection=txt_collection)

    # Create image vector store
    image_store = ChromaVectorStore(chroma_collection=img_collection)

    # Create storage context
    storage_context = StorageContext.from_defaults(vector_store=text_store, image_store=image_store)


    text_documents = []
    for d in documents:
        if isinstance(d, Document):
            text_documents.append(d)

    image_documents = []
    for d in documents:
        if isinstance(d, ImageDocument):
            image_documents.append(d)

    # Parsear documentos a nodos
    node_parser = SentenceSplitter.from_defaults()
    image_nodes = node_parser.get_nodes_from_documents(image_documents)
    text_nodes = node_parser.get_nodes_from_documents(text_documents)


    # Create multimodal index
    index = MultiModalVectorStoreIndex(
    nodes=image_nodes + text_nodes,
    is_image_to_text=True,
    storage_context=storage_context,
    embed_model = text_embed_model,
    image_embed_model=image_embed_model
  
    )


    index.storage_context.persist(persist_dir=persist_dir)

    return index

def load_index(persist_dir: str)->MultiModalVectorStoreIndex:
    """Load index from storage"""
    chroma_client2 = chromadb.PersistentClient(path=persist_dir)
    txt_collection2 = chroma_client2.get_collection(name="text_collection")
    img_collection2 = chroma_client2.get_collection(name="images_collection")
    text_store2 = ChromaVectorStore(chroma_collection=txt_collection2)
    image_store2 = ChromaVectorStore(chroma_collection=img_collection2)
    image_embed_model = ClipEmbedding()
    text_embed_model = NomicEmbedding(api_key=os.getenv('NOMIC_API_KEY'), model_name="nomic-embed-text-v1.5", dimensionality=512)
    storage_contex2 = StorageContext.from_defaults(vector_store=text_store2, image_store=image_store2, persist_dir=persist_dir)
    index2 = load_index_from_storage(storage_contex2, embed_model=text_embed_model, image_embed_model=image_embed_model)
    return index2

def ingestion(txt_image_dir: str, persist_dir: str) -> MultiModalVectorStoreIndex:
    """
    Ingestion function to create a multimodal index from a text directory and an image directory.
    """
    # Load the context images and text
    documents = load_documents(txt_image_dir)

    # Create index
    if os.path.exists(persist_dir):
        print(f"Loading index from ....{persist_dir}")	
        index = load_index(persist_dir)
    else:
        print(f"Creating index...{persist_dir}")
        index = create_multimodal_index(documents, persist_dir)

    return index

