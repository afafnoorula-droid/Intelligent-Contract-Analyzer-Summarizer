from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from app.utils.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, api_key=os.getenv("GROQ_API_KEY"))

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

def get_vector_store():
    Path("chroma_db").mkdir(exist_ok=True)
    return Chroma(persist_directory="chroma_db", embedding_function=embeddings)

def add_to_vector_store(text: str, metadata: dict):
    try:
        vectorstore = get_vector_store()
        chunks = text_splitter.split_text(text)
        vectorstore.add_texts(texts=chunks, metadatas=[metadata] * len(chunks))
        logger.info(f"Added {len(chunks)} chunks to vector store")
    except Exception as e:
        logger.error(f"Vector store error: {e}")

def chat_with_contract(contract_id: str, question: str):
    try:
        vectorstore = get_vector_store()
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=vectorstore.as_retriever(search_kwargs={"k": 8}), memory=memory
        )
        result = qa_chain({"question": f"Contract {contract_id}: {question}"})
        return result["answer"]
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return "Sorry, could not retrieve info."