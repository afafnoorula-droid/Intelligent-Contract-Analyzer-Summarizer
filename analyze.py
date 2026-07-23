from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import uuid
import shutil
from datetime import datetime
import json
import traceback
import re  # ← Added for robust JSON extraction

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

from app.services.document_processor import process_document
from app.services.chains import run_all_chains
from app.services.risk_analyzer import RiskAnalyzer
from app.services.vector_store import add_to_vector_store, chat_with_contract
from app.services.report_generator import generate_pdf_report, generate_word_report
from app.services.comparison import compare_contracts

from app.models.schemas import ContractAnalysisResponse
from app.utils.logger import logger
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api")

# -----------------------------
# Database Setup
# -----------------------------
engine = create_engine("sqlite:///contracts.db", echo=False)
Base = declarative_base()


class ContractDB(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(String, unique=True)
    filename = Column(String)
    risk_score = Column(Integer)
    risk_level = Column(String)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    executive_summary = Column(String)
    key_clauses = Column(String)
    risk_json = Column(String)
    raw_chains_data = Column(String)
    language = Column(String, default="en")


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

risk_analyzer = RiskAnalyzer()


# -----------------------------
# Analyze Contract
# -----------------------------
@router.post("/analyze")
async def analyze_contracts(
    files: list[UploadFile] = File(...),
    current_user=Depends(get_current_user)
):
    results = []
    db = SessionLocal()

    for file in files:
        try:
            contract_id = str(uuid.uuid4())[:12]
            file_path = Path("uploads") / f"{contract_id}_{file.filename}"

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            text = process_document(str(file_path))
            chain_results = run_all_chains(text)

            summary = chain_results.get("summary", "")
            clauses_text = chain_results.get("clauses", "")
            parties_text = chain_results.get("parties", "{}")

            # ==========================
            # DEBUG OUTPUT
            # ==========================
            print("\n================ PARTIES OUTPUT ================\n")
            print(parties_text)
            print("\n================================================\n")

            # === Robust JSON Parsing (Replaced block) ===
            try:
                # Pehle direct JSON parse ki koshish karo
                key_parties = json.loads(parties_text)

            except Exception:
                try:
                    # Agar LLM ne extra text diya ho to usme se JSON extract karo
                    match = re.search(r'```json\s*(\{.*?\})\s*```', parties_text, re.DOTALL)

                    if match:
                        key_parties = json.loads(match.group(1))
                    else:
                        # Agar markdown block nahi mila to normal JSON search karo
                        match = re.search(r'(\{.*\})', parties_text, re.DOTALL)

                        if match:
                            key_parties = json.loads(match.group(1))
                        else:
                            raise Exception("No JSON Found")

                except Exception as e:
                    print("\n================ JSON PARSE FAILED ================")
                    print("ERROR:", e)
                    print("RAW RESPONSE:")
                    print(parties_text)
                    print("===================================================")

                    key_parties = {
                        "party_a": "Not specified",
                        "party_b": "Not specified",
                        "roles": {}
                    }

            risk_result = risk_analyzer.analyze_risks(text)

            result = ContractAnalysisResponse(
                contract_id=contract_id,
                filename=file.filename,
                executive_summary=summary,
                key_parties=key_parties,
                key_clauses={"raw": clauses_text},
                risk_analysis=[r.model_dump() for r in risk_result.risks],
                overall_risk_score=risk_result.overall_risk_score,
                risk_level=risk_result.risk_level,
                red_flags=risk_result.red_flags,
                recommendations=risk_result.recommendations,
                analysis_date=datetime.now(),
                language="en"
            )

            #add_to_vector_store(
                #text,
                #{
                    #"contract_id": contract_id,
                   # "filename": file.filename
              #  }
           # )

           # db_entry = ContractDB(
               # contract_id=contract_id,
               # filename=file.filename,
               # risk_score=result.overall_risk_score,
               # risk_level=result.risk_level,
               # executive_summary=summary,
               # key_clauses=json.dumps(clauses_text),
               # risk_json=json.dumps(risk_result.model_dump()),
               # raw_chains_data=json.dumps(chain_results, default=str),
               # language=result.language
           # )

            #db.add(db_entry)
            #db.commit()

           # pdf_path = generate_pdf_report(result)
           # word_path = generate_word_report(result)

            #result.pdf_report = pdf_path
            #result.word_report = word_path

            file_path.unlink(missing_ok=True)

            results.append(result.model_dump())

        except Exception as e:
           print("\n================ FULL ERROR ================\n")
           traceback.print_exc()
           print("\n============================================\n")

           logger.error(traceback.format_exc())

           raise HTTPException(status_code=500, detail=str(e))

    db.close()

    return {
        "status": "success",
        "results": results
    }


# -----------------------------
# Compare Contracts
# -----------------------------
@router.post("/compare")
async def compare(data: dict, current_user=Depends(get_current_user)):
    try:
        return compare_contracts(
            data.get("contract_id1"),
            data.get("contract_id2")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Chat
# -----------------------------
@router.post("/chat")
async def contract_chat(data: dict, current_user=Depends(get_current_user)):
    try:
        answer = chat_with_contract(
            data.get("contract_id"),
            data.get("question")
        )
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# History
# -----------------------------
@router.get("/history")
async def get_history(current_user=Depends(get_current_user)):
    db = SessionLocal()

    records = db.query(ContractDB).all()

    db.close()

    return [
        {
            "contract_id": r.contract_id,
            "filename": r.filename,
            "risk_score": r.risk_score,
            "date": r.analysis_date.isoformat(),
        }
        for r in records
    ]