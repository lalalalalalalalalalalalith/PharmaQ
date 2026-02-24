
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
# EXPANDED SYMPTOM DATABASE
# -----------------------------

symptom_db = {
"fever": "Paracetamol 500–650 mg q6–8h | Hydration | Red flag: >3 days or bleeding",
"high fever": "Paracetamol 650 mg | Monitor temperature | Red flag: >103°F",
"cold": "Cetirizine 10 mg OD | Steam inhalation",
"dry cough": "Dextromethorphan 10–20 mg TID | Warm fluids",
"wet cough": "Ambroxol 30 mg TID | Steam inhalation",
"sore throat": "Warm saline gargles + lozenges",
"nasal congestion": "Xylometazoline spray (max 5 days)",
"breathlessness (mild)": "Levocetirizine 5 mg OD | Monitor",
"wheezing": "Salbutamol inhaler 1–2 puffs",
"sinus pain": "Steam + Paracetamol",
"acidity": "Pantoprazole 40 mg before food",
"gas": "Simethicone as per label",
"diarrhea": "ORS + Zinc 20 mg OD",
"vomiting": "Ondansetron 4 mg SOS",
"constipation": "Isabgol 1–2 tsp HS",
"abdominal cramps": "Drotaverine 40 mg TID",
"piles": "Topical hemorrhoid cream",
"nausea": "Domperidone 10 mg TID",
"headache": "Paracetamol 500 mg | Rest",
"migraine": "Naproxen 250–500 mg",
"dizziness": "ORS + Hydration",
"insomnia": "Melatonin 3–5 mg",
"anxiety (mild)": "Lifestyle modification",
"body pain": "Paracetamol 500 mg",
"joint pain": "Ibuprofen 400 mg",
"back pain": "Diclofenac gel",
"muscle strain": "Ice + NSAID gel",
"fungal infection": "Clotrimazole cream BD",
"rash": "Levocetirizine 5 mg",
"acne": "Benzoyl peroxide OD",
"minor burn": "Silver sulfadiazine topical"
}

# -----------------------------
# EXPANDED DRUG INTERACTIONS
# -----------------------------

interaction_db = {
("warfarin","aspirin"): "Severe – Bleeding risk – Avoid",
("warfarin","metronidazole"): "High – ↑ INR – Monitor INR",
("warfarin","fluconazole"): "High – CYP inhibition – Reduce dose",
("clopidogrel","omeprazole"): "Moderate – Reduced effect – Prefer pantoprazole",
("metformin","contrast media"): "High – Lactic acidosis – Hold 48 hrs",
("ace inhibitor","spironolactone"): "High – Hyperkalemia – Monitor K",
("paracetamol","alcohol"): "Moderate – Hepatotoxicity – Avoid alcohol",
("sildenafil","nitrates"): "Severe – Hypotension – Contraindicated",
("rifampicin","oral contraceptives"): "High – Reduced efficacy – Backup method",
("lithium","nsaids"): "High – Lithium toxicity – Monitor levels",
("digoxin","verapamil"): "High – Digoxin toxicity – Monitor",
("atorvastatin","clarithromycin"): "Moderate – Myopathy risk",
("azithromycin","qt drugs"): "Moderate – QT prolongation – ECG caution",
("fluoxetine","tramadol"): "High – Serotonin syndrome – Avoid",
("insulin","beta blockers"): "Moderate – Mask hypoglycemia – Monitor glucose"
}

# -----------------------------
# PAGE 1: SMART SYMPTOM SEARCH
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
                st.success(f"{match.title()} → {symptom_db[match]}")
        else:
            st.warning("No matching symptom found.")

# -----------------------------
# PAGE 2: DRUG INTERACTION SEARCH
# -----------------------------

if st.session_state.page == "interaction":
    st.subheader("Drug Interaction Checker")

    drug1 = st.text_input("Drug 1").lower()
    drug2 = st.text_input("Drug 2").lower()

    if drug1 and drug2:
        found = False
        for (d1, d2), info in interaction_db.items():
            if (drug1 in d1 and drug2 in d2) or (drug1 in d2 and drug2 in d1):
                st.error(info)
                found = True
                break

        if not found:
            st.success("No major interaction found.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
