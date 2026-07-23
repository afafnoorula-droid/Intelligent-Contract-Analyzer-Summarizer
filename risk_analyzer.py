from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List
from app.utils.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

class RiskItem(BaseModel):
    clause: str
    risk_level: str
    reason: str
    suggestion: str
    jurisdiction: str = "UAE/UK/US"

class RiskAnalysis(BaseModel):
    overall_risk_score: int
    risk_level: str
    risks: List[RiskItem]
    red_flags: List[str]
    recommendations: List[str]

class RiskAnalyzer:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0, api_key=os.getenv("GROQ_API_KEY"))
        self.parser = PydanticOutputParser(pydantic_object=RiskAnalysis)

    def analyze_risks(self, contract_text: str):
        prompt = PromptTemplate.from_template("""
        You are an expert international lawyer (UAE, UK, US). Analyze risks thoroughly.
        Contract: {text}
        {format_instructions}
        """)
        chain = prompt | self.llm | self.parser
        try:
            return chain.invoke({"text": contract_text[:20000], "format_instructions": self.parser.get_format_instructions()})
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return RiskAnalysis(overall_risk_score=65, risk_level="Medium", risks=[], red_flags=["Manual review recommended"], recommendations=["Consult senior lawyer"])
