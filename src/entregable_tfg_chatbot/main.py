from llama_index.core.indices.multi_modal.base import MultiModalVectorStoreIndex
from llama_index.core import PromptTemplate
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from entregable_tfg_chatbot.etl import etl_women
from entregable_tfg_chatbot.ingestion import ingestion
from dotenv import load_dotenv
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core import get_response_synthesizer
from llama_index.llms.ollama import Ollama
from llama_index.core.schema import ImageNode
from translate import Translator
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, Wav2Vec2Processor
import whisper
import librosa
import gradio as gr
import librosa
import torch


_ = load_dotenv()


class RAGStringQueryEngine(CustomQueryEngine):
    """RAG Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm:Ollama
    qa_prompt: PromptTemplate

    def custom_query(self, query: str):
        # Busqueda semantica de nodos relevantes
        nodes = self.retriever.retrieve(query)
        #Extraer el contentido de los nodos
        context_str = "\n\n".join([n.node.get_content() for n in nodes])

        #Generar la respuesta
        response = self.llm.complete(
            self.qa_prompt.format(context_str=context_str, query_str=query)
        )
        return str(response), nodes



def multimodal_rag(index: MultiModalVectorStoreIndex, model:str ='llava:13b', k:int=1):
    """
    Create a Rag Engine from a MultiModalIndex and a LLM.
    """

    # define prompt
    qa_prompt = PromptTemplate(
    "Context information is below.\n"
    "---------------------\n"
    "Context: {context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)

  
    # define the model
    llm = Ollama(model=model, request_timeout=60.0)

    # define response synthesizer
    synthesizer = get_response_synthesizer(response_mode="compact",llm=llm)


    # degine retriever
    retriever = index.as_retriever(similarity_top_k=k, image_similarity_top_k=k)

    # instantiate the query engine
    rag_engine = RAGStringQueryEngine(
    retriever=retriever,
    response_synthesizer=synthesizer,
    llm=llm,
    qa_prompt=qa_prompt,
    )

    return rag_engine

def respond(audio_file):
    query = speech_to_text(audio_file)
    return rag_respond(query)

def speech_to_text(audio_file):
    
  # Loading the audio file
  audio, rate = librosa.load(audio_file)
  
  print(audio_file)
  #printing audio
  print(audio)
  #printing rate
  print(rate)
  
  ## WHISPER MODEL
  #audio = whisper.load_audio(audio_file)  
  model = whisper.load_model("base")
  result = model.transcribe(audio, language = "English", temperature=0.0, fp16=False)
  transcription = result["text"]
  return 'User Question: ' +  transcription

def rag_respond(query):
    global index
    global rag_engine
    response , nodes = rag_engine.custom_query(query)
   
    for n in nodes:
        if isinstance(n.node, ImageNode):
            img = n.node.metadata["file_path"]
        else:
            text = n.node.get_content()
    return   gr.Textbox(query), gr.Textbox(response), gr.Image(img), gr.Textbox(text)


if __name__ == "__main__":
   print('1/4. Ejecutando la etl')
   #etl_women('../../data/store_zara_data/store_zara.csv', '../../data/store_zara_data/images/zara/', '../../data/women_txt_img_tfg/', '../../data/shoes_woman_etl.csv')
   print('2/4. Ejecutando la ingestion de datos multimodal')
   index = ingestion('../../data/women_txt_img/', '../../data/storage_women_dimensionlality_512/')
   print('3/4. Creación del motor de búsqueda multimodal')
   rag_engine = multimodal_rag(index)
   #rag_engine = multimodal_rag(index, model='llama3.2-vision:11b')
   print("4/4. Iniciando el chatbot")
   
   demo = gr.Interface(
    fn = respond,
    inputs = gr.Audio(
        sources = ["upload", "microphone"], 
        format= "wav", 
        type="filepath"),
    outputs=[gr.Textbox(), gr.Textbox(), gr.Image(), gr.Textbox()],
    title = "chatbot",
    description = "Multimodal Chatbot, inlcuding audio question mode"
    )
   
   demo.launch(allowed_paths=['d:\\project_tfg\\pocs\\poc_llamaindex_chromadb\\data\\women_txt_img'])
   