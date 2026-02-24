
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
.toggle-btn {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 30px;
}
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
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
    "fever": "Paracetamol 500–650 mg | Monitor if >3 days | Hydration",
    "viral fever": "Paracetamol + Rest | Monitor platelets if dengue suspected",
    "cold": "Cetirizine 10 mg | Steam inhalation",
    "dry cough": "Dextromethorphan syrup | Warm fluids",
    "wet cough": "Ambroxol | Steam inhalation",
    "acidity": "Pantoprazole 40 mg before food",
    "headache": "Paracetamol | Hydration | Rest",
    "diarrhea": "ORS + Zinc | Monitor dehydration",
    "vomiting": "Ondansetron 4 mg | Oral fluids",
    "constipation": "Isabgol at night | High fiber diet"
}

interaction_db = {
    ("warfarin", "aspirin"): "Severe – Bleeding risk – Avoid or monitor INR",
    ("clopidogrel", "omeprazole"): "Moderate – Reduced antiplatelet effect – Prefer pantoprazole",
    ("metformin", "contrast media"): "High – Lactic acidosis risk – Hold 48 hrs",
    ("sildenafil", "nitrates"): "Severe – Hypotension – Contraindicated",
    ("paracetamol", "alcohol"): "Hepatotoxicity – Avoid alcohol"
}

# -----------------------------
# PAGE 1: SYMPTOM SMART SEARCH
# -----------------------------

if st.session_state.page == "symptom":
    st.subheader("Symptom to OTC Suggestion")

    user_input = st.text_input("Type symptom").lower()

    if user_input:
        # Substring search
        matches = [key for key in symptom_db if user_input in key]

        # If no direct substring match → fuzzy match
        if not matches:
            matches = difflib.get_close_matches(user_input, symptom_db.keys(), n=5, cutoff=0.4)

        if matches:
            st.write("### Results:")
            for match in matches:
                st.success(f"**{match.title()}** → {symptom_db[match]}")
        else:
            st.warning("No matching symptom found.")

# -----------------------------
# PAGE 2: DRUG INTERACTION SMART SEARCH
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
