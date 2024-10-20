import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in environment. Please set it in a .env file.")
    st.stop()

# LangChain imports
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import MapReduceDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.cache import InMemoryCache

# Caching vectorstore as a resource
@st.cache_resource(show_spinner=False)
def load_and_index(data_dir: str, chunk_size: int, chunk_overlap: int):
    """
    Load PDFs from data_dir, split into chunks, build FAISS vectorstore.
    Returns a list of Document chunks.
    """
    # 1. Load docs
    loader_paths = list(Path(data_dir).glob("*.pdf"))
    all_docs = []
    for path in loader_paths:
        loader = PyPDFLoader(str(path))
        docs = loader.load()
        # Attach source metadata
        for d in docs:
            d.metadata["source"] = path.name
        all_docs.extend(docs)

    # 2. Split docs
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(all_docs)
    return chunks

# Streamlit page config
st.set_page_config(page_title="Market Research Synthesizer", page_icon="📰", layout="wide")
st.title("📰 Market Research Synthesizer")

# Sidebar: user settings
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.0, 0.1)
    chunk_size = st.number_input("Chunk size (chars)", min_value=500, max_value=2000, value=800, step=100)
    chunk_overlap = st.number_input("Chunk overlap (chars)", min_value=0, max_value=500, value=150, step=50)
    st.markdown("---")
    st.write("Data folder: **data/raw/** (drop your PDFs here)")

# Main UI
question = st.text_input("Business question", placeholder="e.g. What's new in the European cosmetics market?")

if st.button("Generate summary") and question:
    with st.spinner("Loading documents & building index..."):
        chunks = load_and_index("data/raw", chunk_size, chunk_overlap)
    st.success(f"Loaded {len(chunks)} chunks from {len(Path('data/raw').glob('*.pdf'))} documents.")

    # Define prompts
    map_prompt = PromptTemplate(
        input_variables=["page_content", "metadata"],
        template="""
You are a research assistant.
Summarize the following excerpt, adding a citation tag [SourceName, p.PageNumber] at the end.

Excerpt:
{page_content}

Metadata: {metadata}
"""
    )
    reduce_prompt = PromptTemplate(
        input_variables=["summaries"],
        template="""
You are a head analyst.
Combine these mini-summaries into a concise executive summary, preserving citation tags.

Summaries:
{summaries}
"""
    )

    # Build and run MapReduce chain
    with st.spinner("Running Map-Reduce summarization..."):
        chain = MapReduceDocumentsChain(
            llm=OpenAI(temperature=temperature),
            map_prompt=map_prompt,
            reduce_prompt=reduce_prompt
        )
        result = chain.run(chunks)

    # Display results
    st.subheader("Executive Summary with Citations")
    st.markdown(result)

    # (Optional) Download as PPTX stub
    st.download_button(
        label="Download PPTX (coming soon)",
        data=None,
        file_name="summary.pptx",
        disabled=True
    )
else:
    st.info("Enter a question above and click **Generate summary** to start.")
