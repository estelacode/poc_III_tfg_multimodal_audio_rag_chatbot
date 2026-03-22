#### TFG - Redesigning the User Experience with Artificial Intelligence: Fashion Industry Specialized Chatbot
## Poc III: Multimodal RAG Chatbot (Audio)


## Overview 
A multimodal RAG (Retrieval-Augmented Generation) chatbot specialized in the fashion domain, designed to process user queries in text or audio and return responses combining text and images. The system retrieves semantically relevant products from a multimodal vector store built from the Store Zara dataset, which includes both product metadata and associated images.

The architecture leverages Chroma as a persistent multimodal vector database, Nomic for text embeddings, and OpenCLIP for image embeddings. Multimodal reasoning is performed using LLaVA 1.6 (7B/13B) and LLaMA 3.2 Vision (11B) served via Ollama. The application integrates an ETL pipeline for dataset preparation, a data ingestion pipeline for indexing, and an interactive Gradio-based user interface.

## Demo


## Features
- Multimodal chatbot: supports text and audio input, and returns text + images
- Multimodal RAG architecture for context-aware responses
- Persistent multimodal vector store using Chroma
- Semantic retrieval across product descriptions and images
- Image embeddings using OpenCLIP
- Text embeddings using Nomic (nomic-embed-text-v1.5)
- Large Multimodal Models: LLaVA 1.6 (7B/13B) and LLaMA 3.2 Vision (11B)
- Voice query support via Whisper (Speech-to-Text)
- Exploration of Text-to-Speech (TTS) capabilities
- ETL pipeline for automated dataset preprocessing
- Support for multiple image results per query
- Interactive web UI built with Gradio

## Architecture

### `Sequence Diagram`

#### Sequence Flow:
1. User submits a query (text or audio) via the Frontend.
2. If the input is audio, it is transcribed into text using Whisper.
3. Frontend sends the query to the Backend.
4. Backend generates query embeddings (Nomic for text).
5. Backend performs semantic search in the Multimodal Vector Store (Chroma) using text and image embeddings (OpenCLIP).
6. Backend retrieves the most relevant product data (text + images).
7. Backend sends the query along with the retrieved context to the Ollama Multimodal LLM (LLaVA 1.6 or LLaMA 3.2 Vision).
8. LLM generates a multimodal response based on the provided context.
9. Backend returns the generated response to the Frontend.
10. Frontend displays the response (text and multiple images) to the user.

## Tech Stack

## Setup
```bash
# 1. Install Poetry (required) - https://python-poetry.org/docs/#installing-with-the-official-installer
# Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
poetry --version

# 2. Clone the repository
git clone https://github.com/estelacode/poc_tfg_chatbot_texto.git
cd entregable_tfg_chatbot

# 3. Select the Python interpreter for this project
poetry env use /full/path/to/python
# Example for Windows:
# poetry env use C:\Users\emada\AppData\Local\Programs\Python\Python312


# 4. Install dependencies
poetry install
## Usage
```bash
# Run the project
poetry run python src/entregable_tfg_chatbot/main.py
```

## Project Structure
```bash
ENTREGABLE_TFG_CHATBOT/
├── data/                     # Data files
├── demo_interface/           # Demo interface or media
├── notebooks/                # Jupyter notebooks for experiments
├── src/                      # Source code 
├── vectorstore/              # Vector database storage 
├── .env                      # Environment variables (keep secret)
├── .gitignore                # Git ignore rules
├── poetry.lock               # Poetry dependency lock file
├── pyproject.toml            # Poetry configuration and dependencies
└── README.md                 # Project README file
```
## Roadmap
- Improve retrieval accuracy using hybrid search (semantic + metadata filtering)
- Implement reranking techniques to refine multimodal results
- Expand dataset with a larger and more diverse fashion catalog
- Introduce evaluation metrics (e.g., Recall@k, precision) to measure system performance
- Improve Speech-to-Text accuracy for more reliable voice queries
Implement guardrails and topic filtering for safer and more controlled outputs
- Deploy the application as a scalable cloud service (Docker + API)

## References
- [Poetry Documentation](https://python-poetry.org/docs/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [LlamaIndex RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/)
- [Nomic](https://www.nomic.ai/developer)
- [Ollama](https://ollama.com/)
- [Gradio](https://www.gradio.app/guides/quickstart)

### 👋 Author
Estela Madariaga


