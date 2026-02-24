
import streamlit as st
import difflib
import re

st.set_page_config(page_title="PHARMAQ", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp { background-color: #0f1b2b; }
.main-title {
    font-size: 46px;
    font-weight: 800;
    text-align: center;
    color: #4ea8de;
}
.card {
    background-color: #f4f6f9;
    padding: 20px;
    border-radius: 10px;
    margin-top: 15px;
}
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)

# ---------------- PAGE TOGGLE ----------------
if "page" not in st.session_state:
    st.session_state.page = "symptom"

c1, c2 = st.columns(2)
with c1:
    if st.button("🩺 Symptom to OTC"):
        st.session_state.page = "symptom"
with c2:
    if st.button("💊 Drug Interaction Checker"):
        st.session_state.page = "interaction"

st.divider()

# ---------------- BUILD SYMPTOM ----------------
def build_symptom(cause, otc):
    return {
        "Cause": cause,
        "OTC": otc,
        "Advice": "Hydration, rest, monitor symptoms.",
        "Red Flag": "Persistent >3 days or worsening."
    }

# ---------------- SYMPTOM DATABASE (UNCHANGED) ----------------
symptom_db = {
"fever": build_symptom("Viral infection","Paracetamol"),
"cold": build_symptom("Viral URI","Cetirizine"),
"headache": build_symptom("Tension","Paracetamol"),
"body pain": build_symptom("Viral","Paracetamol"),
"acidity": build_symptom("GERD","Pantoprazole"),
"diarrhea": build_symptom("Viral","ORS + Zinc"),
"vomiting": build_symptom("Gastritis","Ondansetron"),
}

combo_db = {
frozenset(["fever","cold"]): "Likely viral URTI – Paracetamol + Cetirizine",
frozenset(["fever","headache"]): "Viral fever pattern – Paracetamol",
frozenset(["diarrhea","vomiting"]): "Gastroenteritis – ORS + Zinc + Ondansetron"
}

# ---------------- INTERACTION DATABASE (UNCHANGED) ----------------
interaction_db = {
frozenset(["paracetamol","alcohol"]):("Moderate","Liver toxicity","Avoid alcohol"),
frozenset(["warfarin","aspirin"]):("Severe","Bleeding risk","Avoid combination"),
frozenset(["sildenafil","nitrates"]):("Severe","Severe hypotension","Contraindicated"),
frozenset(["metformin","contrast media"]):("High","Lactic acidosis","Hold 48 hrs"),
}

# Precompute drug list
all_drugs = sorted({drug for pair in interaction_db for drug in pair})

# ---------------- NORMALIZATION HELPERS ----------------
def smart_split(text):
    return [t.strip() for t in re.split(r',|and|\s+', text) if t.strip()]

def normalize_term(term, database_keys):
    # Exact
    if term in database_keys:
        return term

    # Partial
    partial = [k for k in database_keys if term in k]
    if partial:
        return partial[0]

    # Fuzzy
    fuzzy = difflib.get_close_matches(term, database_keys, n=1, cutoff=0.6)
    if fuzzy:
        return fuzzy[0]

    return None

# ---------------- SYMPTOM PAGE ----------------
if st.session_state.page == "symptom":
    user_input = st.text_input("Type symptom (comma, space, or 'and')").lower().strip()

    if user_input:
        parts = smart_split(user_input)

        if len(parts) > 1:
            normalized = []
            for p in parts:
                match = normalize_term(p, symptom_db.keys())
                if match:
                    normalized.append(match)

            if len(normalized) >= 2:
                key = frozenset(normalized[:2])
                if key in combo_db:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.write(combo_db[key])
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Combination not found.")
            else:
                st.error("Could not identify symptoms clearly.")
        else:
            term = normalize_term(parts[0], symptom_db.keys())
            if term:
                data = symptom_db[term]
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(f"### {term.title()}")
                for k,v in data.items():
                    st.write(f"**{k}:** {v}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Symptom not found.")

# ---------------- INTERACTION PAGE ----------------
if st.session_state.page == "interaction":
    user_input = st.text_input("Type two drugs (comma, space, or 'and')").lower().strip()

    if user_input:
        parts = smart_split(user_input)

        if len(parts) >= 2:
            d1 = normalize_term(parts[0], all_drugs)
            d2 = normalize_term(parts[1], all_drugs)

            if not d1 or not d2:
                st.error("Could not identify both drugs clearly.")
            elif d1 == d2:
                st.warning("Please enter two different drugs.")
            else:
                key = frozenset([d1, d2])
                if key in interaction_db:
                    sev, mech, adv = interaction_db[key]
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.write(f"**Severity:** {sev}")
                    st.write(f"**Mechanism:** {mech}")
                    st.write(f"**Advice:** {adv}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.success("No major interaction found.")
        else:
            st.warning("Please enter two drug names.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
