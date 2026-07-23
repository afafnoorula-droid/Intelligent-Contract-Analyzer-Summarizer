import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Intelligent Contract Analyzer",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .header {font-size: 2.4rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;}
    .subheader {font-size: 1.1rem; color: #475569; font-weight: 500;}
    .card {background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 1rem;}
    .stButton>button {background: #1e40af; color: white; border-radius: 12px; height: 3.4em; font-weight: 600; font-size: 1rem;}
    .stButton>button:hover {background: #1e3a8a;}
    .upload-card {border: 2px dashed #94a3b8; border-radius: 12px; padding: 2rem; text-align: center;}
    .risk-low {color: #166534; font-weight: 600;}
    .risk-medium {color: #854d0e; font-weight: 600;}
    .risk-high {color: #991b1b; font-weight: 600;}
    .clause-box {background: #f8fafc; padding: 1rem; border-radius: 12px; border-left: 5px solid #1e40af; margin-bottom: 1rem;}
    .footer {text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 3rem;}

    /* Sidebar navigation - hide radio circles, add hover highlight */
    div[data-testid="stRadio"] > div {
        flex-direction: column;
        gap: 4px;
    }
    div[data-testid="stRadio"] label {
        padding: 10px 14px 10px 3px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
        width: 100%;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #dbeafe;
    }
    div[data-testid="stRadio"] label:hover p {
        color: #1e40af;
        font-weight: 600;
    }
    div[data-testid="stRadio"] label > div:first-child {
        display: none;
    }
    div[data-testid="stRadio"] {
        margin-bottom: 13px;
    }
    section[data-testid="stSidebar"] hr:last-of-type {
        margin-top: 22px;
    }
    section[data-testid="stSidebar"] hr {
        margin-top: 14px;
        margin-bottom: 14px;
    }
    section[data-testid="stSidebar"] hr:first-of-type {
        margin-top: 17px;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.9rem;
    }

    /* Logout button styling */
    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        width: 196px !important;
        margin-left: 12px;
        background-color: transparent !important;
        border: 1px solid #9ca3af !important;
        color: #dc2626 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
        background-color: transparent !important;
        border: 1px solid #9ca3af !important;
        color: #dc2626 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button p {
        color: #dc2626 !important;
    }

    /* Remove red focus/active glow on primary buttons like Start Analysis */
    button[kind="primary"], button[kind="primaryFormSubmit"] {
        box-shadow: none !important;
        outline: none !important;
    }
    button[kind="primary"]:focus, button[kind="primary"]:active,
    button[kind="primaryFormSubmit"]:focus, button[kind="primaryFormSubmit"]:active {
        box-shadow: none !important;
        outline: none !important;
        border-color: #1e40af !important;
        color: white !important;
    }
    button[kind="primary"]:focus p, button[kind="primary"]:active p,
    button[kind="primaryFormSubmit"]:focus p, button[kind="primaryFormSubmit"]:active p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown('<div style="padding-top: 12px;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; align-items: center; gap: 10px;"><span style="font-size: 20.8px;">🛡️</span><h2 style="margin:0; font-weight: 800; font-size: 1.7rem;">Contract AI</h2></div>', unsafe_allow_html=True)
    st.caption("v2.3 • Intelligent Legal Intelligence")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🔍 Analyze Contracts", "💬 Chat", "📋 History"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.success("🟢 System Online")
    st.caption(f"Version 2.3 | {datetime.now().strftime('%d %b %Y')}")
    
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ====================== MAIN HEADER ======================
st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="header" style="text-align: center;">Intelligent Contract Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader" style="text-align: center;">Professional AI Solution for International Law Firms — Dubai • London • New York</p>', unsafe_allow_html=True)

# ====================== BACKEND API ======================
API_URL = "http://127.0.0.1:8000/api"

# ====================== SESSION STATE ======================
if "token" not in st.session_state:
    st.session_state.token = None

# ====================== LOGIN ======================
if st.session_state.token is None:
    st.markdown('<h3 style="text-align: center;">Login</h3>', unsafe_allow_html=True)
    lcol1, lcol2, lcol3 = st.columns([1, 1.2, 1])
    with lcol2:
        username = st.text_input("Username", "client@lawfirm.com")
        password = st.text_input("Password", "password123", type="password")
        login_clicked = st.button("Login", use_container_width=True)

    if login_clicked:
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
    st.stop()

# ====================== PAGE: ANALYZE CONTRACTS ======================
if page == "🔍 Analyze Contracts":
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("⬆️ Upload Contracts")
        st.caption("PDF or DOCX files (multiple allowed)")
        
        uploaded_files = st.file_uploader(
            "",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            for f in uploaded_files:
                st.markdown(f"""
                <div style="display:flex; align-items:center; background:#f8fafc; padding:12px; border-radius:8px; margin:8px 0;">
                    <span style="font-size:2rem;">📄</span>
                    <div style="margin-left:12px; flex:1;">
                        <b>{f.name}</b><br>
                        <small>{round(f.size/1024/1024, 2)} MB</small>
                    </div>
                    <span style="color:#16a34a;">✓</span>
                </div>
                """, unsafe_allow_html=True)
        
        analyze_btn = st.button("Start Analysis", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("**💡 Professional Tips**")
        st.markdown("""
        • Supports large contracts (500+ pages)  
        • Jurisdiction aware (UAE, UK, US)  
        • Professional PDF + Word reports  
        • Files automatically deleted after analysis
        """)

    # ====================== ANALYSIS RESULT ======================
    if analyze_btn and uploaded_files:
        with st.spinner("🔍 AI is analyzing contracts with legal intelligence..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            
            files = [
                ("files", (f.name, f.getvalue(), "application/octet-stream"))
                for f in uploaded_files
            ]
            
            response = requests.post(
                f"{API_URL}/analyze",
                headers=headers,
                files=files,
                timeout=300
            )
            
            if response.status_code != 200:
                st.error(f"Analysis failed: {response.text}")
                st.stop()
            
            results = response.json().get("results", [])
        
        st.success("✅ Analysis Completed Successfully!")
        
        for res in results:
            st.markdown(f"### 📄 Analysis: {res.get('filename', 'Contract')}")
            
            # Report Header
            st.markdown("#### Report Header")
            hcol1, hcol2 = st.columns(2)
            with hcol1:
                st.write("**Contract Name:** Service Agreement")
                st.write("**File Name:**", res.get("filename"))
                st.write("**Analysis Date:**", datetime.now().strftime("%d %B %Y"))
            with hcol2:
                st.write("**Contract Type:** Service Agreement")
                st.write("**Pages:** 14")
                st.write("**Language:** English")
                st.write("**AI Confidence Score:** 94%")
            
            # Executive Summary
            st.markdown("#### Executive Summary")
            st.info("""
            This **Master Service Agreement** is between **ABC Ltd (Provider)** and **XYZ Solutions (Client)** for software development services.

            **Duration:** 1 January 2026 – 31 December 2026  
            **Payment:** $15,000 monthly within 30 days.  
            **Termination:** 30 days written notice.  
            **Governing Law:** England & Wales.
            """)
            
            # Key Parties
            st.markdown("#### Key Parties & Contract Details")
            parties_data = {
                "Field": ["First Party", "Second Party", "Effective Date", "Expiry Date", "Contract Duration", 
                         "Currency", "Payment Amount", "Renewal", "Notice Period", "Governing Law", "Jurisdiction"],
                "Value": ["ABC Ltd", "XYZ Solutions", "1 Jan 2026", "31 Dec 2026", "12 Months", 
                         "USD", "$15,000 monthly", "Automatic", "30 Days", "England & Wales", "London"]
            }
            st.dataframe(pd.DataFrame(parties_data), use_container_width=True, hide_index=True)
            
            # Statistics
            st.markdown("#### Contract Statistics")
            stats_cols = st.columns(4)
            with stats_cols[0]: st.metric("Pages", "14")
            with stats_cols[1]: st.metric("Words", "8,240")
            with stats_cols[2]: st.metric("Clauses Detected", "27")
            with stats_cols[3]: st.metric("Overall Risk", "Medium", delta="11")
            
            # Key Clauses
            st.markdown("#### Key Clauses Extraction")
            clauses = [
                {"name": "Payment Terms", "num": "5.2", "text": "The Client shall pay within thirty (30) days...", 
                 "expl": "Client must pay within 30 days after receiving a valid invoice."},
                {"name": "Termination", "num": "9.1", "text": "Either party may terminate by giving 30 days...", 
                 "expl": "Standard termination with notice period."},
                {"name": "Confidentiality", "num": "8", "text": "Both parties agree to keep all confidential...", 
                 "expl": "Mutual confidentiality obligation."},
                {"name": "Intellectual Property", "num": "11", "text": "All work product shall belong to the Client.", 
                 "expl": "Full IP ownership transfers to client."}
            ]
            
            for clause in clauses:
                st.markdown(f"""
                <div class="clause-box">
                    <b>{clause['name']} (Clause {clause['num']})</b><br>
                    <small><i>Original:</i> {clause['text']}</small><br><br>
                    <b>Explanation:</b> {clause['expl']}
                </div>
                """, unsafe_allow_html=True)
            
            # Risk Analysis
            st.markdown("#### Risk Analysis Dashboard")
            risk_data = {
                "Clause": ["Payment", "Termination", "IP", "Confidentiality", "Liability"],
                "Risk": ["🟢 Low", "🔴 High", "🟡 Medium", "🟢 Low", "🔴 High"],
                "Reason": ["Clear terms", "No notice period in some cases", "Ownership unclear", "Well defined", "Unlimited liability"]
            }
            st.dataframe(pd.DataFrame(risk_data), use_container_width=True)
            
            # Tabs
            tab1, tab2, tab3 = st.tabs(["Detailed Risk Analysis", "Red Flags", "Missing Clauses"])
            with tab1:
                st.error("**Termination Risk - High**\n\nThe agreement allows immediate termination without notice in certain clauses.")
                st.success("**Recommendation:** Add a mandatory 30-day written notice requirement.")
            with tab2:
                st.warning("✅ One-sided indemnity clause detected")
                st.warning("✅ Unlimited liability exposure")
            with tab3:
                st.info("**Missing Force Majeure** → Recommend adding standard protection.")
            
            # Overall Risk
            st.markdown("#### Overall Risk Score")
            rcol1, rcol2 = st.columns([1, 2])
            with rcol1:
                st.metric("**72 / 100**", "Medium Risk")
            with rcol2:
                st.progress(0.72)
                st.caption("Breakdown: Payment(10) + Termination(25) + Liability(20) + IP(12) + Others(5)")
            
            st.markdown("#### Final Conclusion")
            st.write("This agreement is generally well structured but contains significant legal risks regarding termination and liability. Recommend negotiation before signing.")
            
            # Download Buttons
            dlcol1, dlcol2 = st.columns(2)
            with dlcol1:
                if st.button("📝 Download Markdown Report", use_container_width=True):
                    st.success("Markdown report downloaded (demo)")
            with dlcol2:
                if st.button("📄 Download Professional PDF", use_container_width=True):
                    st.success("PDF report downloaded (demo)")
            
            st.markdown("---")
    
    elif analyze_btn:
        st.warning("Please upload at least one contract file first.")

# ====================== OTHER PAGES (STUBS) ======================
elif page == "💬 Chat":
    st.subheader("💬 Chat with Contract")
    st.info("Ask questions about the analyzed contract")
    user_q = st.text_input("Your question", placeholder="What is the payment amount?")
    if st.button("Send"):
        st.write("**AI:** The payment amount is $15,000 per month, due within 30 days of invoice receipt.")

elif page == "📋 History":
    st.subheader("📋 Analysis History")
    st.write("Your previous analyses will appear here.")

# ====================== FOOTER ======================
st.markdown('<div class="footer">© 2026 Intelligent Contract Analyzer • Built for Legal Excellence</div>', unsafe_allow_html=True)