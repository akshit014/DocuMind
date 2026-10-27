# DocuMind

RAG-based document Q&A: pypdf -> word-window chunks -> MiniLM embeddings -> ChromaDB -> Gemini with cited answers.

## Run
    pip install -r requirements.txt
    export GEMINI_API_KEY=your_key      # Windows: set GEMINI_API_KEY=your_key
    streamlit run app.py

Set GEMINI_MODEL to change the model (default gemini-2.0-flash).

## Layout
- config.py: settings
- loaders.py: file -> pages
- chunking.py: pages -> chunks
- store.py: embeddings + ChromaDB
- rag.py: retrieve + prompt + Gemini
- app.py: Streamlit UI
