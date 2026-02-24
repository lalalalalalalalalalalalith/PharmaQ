
import streamlit as st
import difflib

st.set_page_config(page_title="PHARMAQ", layout="wide")

# -----------------------------
# STYLE
# -----------------------------

st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: #0a3d62;
}
.info-card {
    background-color: #f4f7fb;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
.result-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 20px;
}
.disclaimer {
    background-color: #f8d7da;
    padding: 15px;
    border-radius: 8px;
    margin-top: 30px;
    font-size: 14px;
}
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
}
.stButton>button {
    background-color: #0a3d62;
    color: white;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    transition: 0.2s;
}
.stButton>button:hover {
    background-color: #145374;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)

# -----------------------------
# TOGGLE PAGE SYSTEM
# -----------------------------

if "page" not in st.session_state:
    st.session_state.page = "symptom"

col1, col2 = st.columns(2)

with col1:
    if st.button("🩺 Symptom to OTC"):
        st.session_state.page = "symptom"

with col2:
    if st.button("💊 Drug Interaction Checker"):
        st.session_state.page = "interaction"

st.divider()

# -----------------------------
# DATABASE
# -----------------------------

symptom_db = {
"fever": "Paracetamol 500–650 mg q6–8h | Hydration | Red flag: >3 days or bleeding",
"high fever": "Paracetamol 650 mg | Monitor temperature | Red flag: >103°F",
"cold": "Cetirizine 10 mg OD | Steam inhalation",
"dry cough": "Dextromethorphan 10–20 mg TID | Warm fluids",
"wet cough": "Ambroxol 30 mg TID | Steam inhalation",
"sore throat": "Warm saline gargles + lozenges",
"nasal congestion": "Xylometazoline spray (max 5 days)",
"acidity": "Pantoprazole 40 mg before food",
"diarrhea": "ORS + Zinc 20 mg OD",
"vomiting": "Ondansetron 4 mg SOS",
"constipation": "Isabgol 1–2 tsp HS"
}

interaction_db = {
("warfarin","aspirin"): "Severe – Bleeding risk – Avoid",
("clopidogrel","omeprazole"): "Moderate – Reduced effect – Prefer pantoprazole",
("metformin","contrast media"): "High – Lactic acidosis – Hold 48 hrs",
("sildenafil","nitrates"): "Severe – Hypotension – Contraindicated",
("paracetamol","alcohol"): "Moderate – Hepatotoxicity – Avoid alcohol"
}

# -----------------------------
# PAGE 1: SYMPTOM SEARCH
# -----------------------------

if st.session_state.page == "symptom":
    st.subheader("Symptom to OTC Suggestion")

    user_input = st.text_input("Type symptom").lower()

    if user_input:
        matches = [key for key in symptom_db if user_input in key]

        if not matches:
            matches = difflib.get_close_matches(user_input, symptom_db.keys(), n=5, cutoff=0.4)

        if matches:
            for match in matches:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.success(f"{match.title()} → {symptom_db[match]}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No matching symptom found.")

    # HOW TO USE PANEL (Option 1)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 📘 How to Use PharmaQ")
    st.markdown("""
    • Type symptoms naturally (e.g. fever, cough)  
    • Review OTC suggestions carefully  
    • Always check red flags  
    • Consult a doctor if symptoms persist
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # DISCLAIMER (Option 4)
    st.markdown('<div class="disclaimer">', unsafe_allow_html=True)
    st.markdown("⚠ This tool provides primary care guidance only. It is not a substitute for professional medical consultation.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# PAGE 2: DRUG INTERACTION CHECKER
# -----------------------------

if st.session_state.page == "interaction":
    st.subheader("Drug Interaction Checker")

    drug1 = st.text_input("Drug 1").lower()
    drug2 = st.text_input("Drug 2").lower()

    if drug1 and drug2:
        found = False
        for (d1, d2), info in interaction_db.items():
            if (drug1 in d1 and drug2 in d2) or (drug1 in d2 and drug2 in d1):
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.error(info)
                st.markdown('</div>', unsafe_allow_html=True)
                found = True
                break

        if not found:
            st.success("No major interaction found.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
