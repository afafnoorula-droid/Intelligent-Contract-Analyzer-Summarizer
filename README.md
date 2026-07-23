# 🛡️ Intelligent Contract Analyzer & Summarizer

**Professional AI-Powered Contract Intelligence Platform**  
**Built for International Law Firms**

---

### **Overview**

An intelligent, fast, and secure contract analysis system designed for high-volume law firms in **Dubai, London, and New York**. It reduces manual contract review time by **70-80%** while maintaining high accuracy and professional standards.

---

### **Key Features**

#### **Core Capabilities**
- **Multi-Format Support**: PDF & Word (.docx) — Single & Batch Processing
- **Smart Executive Summary**: Clear, concise 1-page summary with key obligations
- **Automatic Clause Extraction**: Payment Terms, Termination, Confidentiality, Liability, IP, Governing Law, Dispute Resolution
- **Advanced Risk Analysis**: Red / Yellow / Green flagging with jurisdiction awareness (UAE Civil Code, UK, US Common Law)
- **Red Flags Detection**: One-sided clauses, missing protections, ambiguous language
- **AI Recommendations**: Practical improvement suggestions for each risk

#### **Enterprise Features**
- **Bilingual Support**: English + Arabic (العربية)
- **Professional Reports**: Beautiful PDF + Editable Word (.docx) export
- **Contract Comparison**: Side-by-side difference analysis
- **RAG Chat Interface**: Ask questions about any analyzed contract
- **Analysis History & Dashboard**: Track all previous reviews
- **Secure & Private**: Temporary file storage with auto-deletion

#### **Technical Excellence**
- Fast response (<45 seconds for average contracts)
- Built with **FastAPI + LangChain + Groq + Chroma**
- Docker-ready deployment
- Robust error handling & logging

---

### **Screenshots**  

![image alt](https://github.com/afafnoorula-droid/Intelligent-Contract-Analyzer-Summarizer/blob/716fad9b6aba77a87a6b4b303655ee4a938110cb/Screenshot%20(910).png)

![image alt](https://github.com/afafnoorula-droid/Intelligent-Contract-Analyzer-Summarizer/blob/238c78e00cdda27032bf0f8e650ae37aa81390b8/Screenshot%20(911).png)

![image alt](https://github.com/afafnoorula-droid/Intelligent-Contract-Analyzer-Summarizer/blob/ceaf982b64dea9f92f41ccdb88e3a2251fc4f8f3/Screenshot%20(912).png)

![image alt](https://github.com/afafnoorula-droid/Intelligent-Contract-Analyzer-Summarizer/blob/0b9e738a26e3b2e602e6fe83679ea5546a2be8c9/Screenshot%20(913).png)

![image alt](https://github.com/afafnoorula-droid/Intelligent-Contract-Analyzer-Summarizer/blob/b39e4d89cddb39e961eb8dd4c5c10e66e44c7a1d/Screenshot%20(914).png)

![image alt](https://github.com/afafnoorula-droid/Intelligent-Contract-Analyzer-Summarizer/blob/81daee564cb970b3fb53a5a544553057016e5ec0/Screenshot%20(915).png)




### **Quick Setup**

```bash
# 1. Clone / Extract Project
# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Start Backend
uvicorn main:app --reload --port 8000

# 5. Start Frontend (in new terminal)
streamlit run frontend/streamlit_app.py


