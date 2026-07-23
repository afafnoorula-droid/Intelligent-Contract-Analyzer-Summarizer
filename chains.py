from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, api_key=os.getenv("GROQ_API_KEY"))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=300)

def create_key_parties_chain():
    prompt = PromptTemplate.from_template("""
You are an API.

Extract the contract parties.

Return ONLY valid JSON.

Do NOT write:
- Here is the JSON
- Explanation
- Notes
- Markdown
- ```json

Return exactly this format:

{{
  "party_a":"...",
  "party_b":"...",
  "roles":{{
      "party_a_role":"...",
      "party_b_role":"..."
  }}
}}

Contract:

{text}
""")

    return prompt | llm | StrOutputParser()

def create_summary_chain():
    prompt = PromptTemplate.from_template("Give a clear executive summary (max 400 words) in English and Arabic summary:\n\n{text}")
    return prompt | llm | StrOutputParser()

def create_clauses_chain():
    prompt = PromptTemplate.from_template("""Extract key clauses (UAE, UK, US jurisdiction aware):
- Payment Terms
- Termination
- Confidentiality
- Liability & Indemnity
- Intellectual Property
- Governing Law
- Dispute Resolution
Contract: {text}""")
    return prompt | llm | StrOutputParser()

def create_risk_chain():
    prompt = PromptTemplate.from_template("""Analyze risks with jurisdiction awareness (UAE Civil Code, UK, US).
Return JSON only.
Contract: {text}""")
    return prompt | llm | StrOutputParser()

def run_all_chains(text: str):
    chunks = text_splitter.split_text(text)
    processed = " ".join(chunks[:10])
    parallel = RunnableParallel({
        "summary": create_summary_chain(),
        "clauses": create_clauses_chain(),
        "risk": create_risk_chain(),
        "parties": create_key_parties_chain()
    })
    return parallel.invoke({"text": processed}) 
        
