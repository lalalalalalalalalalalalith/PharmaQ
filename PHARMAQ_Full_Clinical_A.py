
import streamlit as st
import difflib
import re

st.set_page_config(page_title="PHARMAQ", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background-color: #0f1b2b; }
.title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: #4ea8de;
}
.card {
    background-color: #f4f6f9;
    padding: 22px;
    border-radius: 12px;
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

st.markdown('<div class="title">PHARMAQ</div>', unsafe_allow_html=True)

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

# ---------- DATA BUILDERS ----------
def build_symptom(cause, otc):
    return {
        "Cause": cause,
        "OTC": otc,
        "Adult Dose": "As per label / standard dosing",
        "Pediatric Dose": "Weight-based if applicable",
        "Tips": "Hydration, adequate rest, monitor symptoms.",
        "Do's": "Follow label instructions, complete full course if prescribed.",
        "Don'ts": "Avoid overdose or combining similar drugs.",
        "When to Consult Doctor": "If symptoms persist >3 days or worsen.",
        "Red Flag": "Severe symptoms, persistent high fever, dehydration."
    }

# ---------- 40 SYMPTOMS ----------
symptom_db = {
"fever": build_symptom("Viral infection","Paracetamol"),
"cold": build_symptom("Viral URI","Cetirizine"),
"headache": build_symptom("Tension","Paracetamol"),
"body pain": build_symptom("Myalgia","Ibuprofen"),
"acidity": build_symptom("GERD","Pantoprazole"),
"diarrhea": build_symptom("Infection","ORS + Zinc"),
"vomiting": build_symptom("Gastritis","Ondansetron"),
"cough": build_symptom("URI","Dextromethorphan"),
"sore throat": build_symptom("Infection","Lozenges"),
"gas": build_symptom("Dyspepsia","Simethicone"),
"dizziness": build_symptom("Vertigo","Meclizine"),
"allergy": build_symptom("Allergic response","Cetirizine"),
"back pain": build_symptom("Muscle strain","Ibuprofen"),
"toothache": build_symptom("Dental issue","Paracetamol"),
"ear pain": build_symptom("Otitis","Paracetamol"),
"eye redness": build_symptom("Allergy","Lubricant drops"),
"constipation": build_symptom("Low fiber","Isabgol"),
"burning urination": build_symptom("UTI suspicion","Hydration"),
"insomnia": build_symptom("Stress","Melatonin"),
"anxiety": build_symptom("Stress","Consultation advised"),
"rash": build_symptom("Dermatitis","Calamine"),
"itching": build_symptom("Allergy","Cetirizine"),
"menstrual pain": build_symptom("Dysmenorrhea","Mefenamic acid"),
"migraine": build_symptom("Neurovascular","Sumatriptan"),
"sunburn": build_symptom("UV exposure","Aloe gel"),
"nausea": build_symptom("Gastritis","Ondansetron"),
"ulcer pain": build_symptom("Peptic ulcer","Pantoprazole"),
"weakness": build_symptom("Fatigue","Multivitamin"),
"joint pain": build_symptom("Arthralgia","Ibuprofen"),
"muscle cramps": build_symptom("Electrolyte imbalance","ORS"),
"dehydration": build_symptom("Fluid loss","ORS"),
"nasal congestion": build_symptom("Cold","Oxymetazoline"),
"sinus pain": build_symptom("Sinusitis","Steam inhalation"),
"ear blockage": build_symptom("Wax","Ear drops"),
"mouth ulcer": build_symptom("Aphthous ulcer","Topical gel"),
"hair fall": build_symptom("Nutritional","Biotin"),
"dry skin": build_symptom("Low hydration","Moisturizer"),
"minor burn": build_symptom("Thermal injury","Silver sulfadiazine"),
"cuts": build_symptom("Minor injury","Antiseptic"),
"bruises": build_symptom("Minor trauma","Cold compress"),
}

# ---------- 20 COMBINATIONS ----------
combo_db = {
frozenset(["fever","cold"]): "Likely viral URTI – Paracetamol + Cetirizine",
frozenset(["fever","headache"]): "Viral fever pattern – Paracetamol",
frozenset(["diarrhea","vomiting"]): "Gastroenteritis – ORS + Zinc + Ondansetron",
frozenset(["cough","cold"]): "Common cold – Antihistamine + cough syrup",
frozenset(["back pain","body pain"]): "Musculoskeletal strain – NSAID",
frozenset(["rash","itching"]): "Allergic dermatitis – Antihistamine",
frozenset(["gas","acidity"]): "Dyspepsia – PPI + Simethicone",
frozenset(["nasal congestion","sinus pain"]): "Sinusitis pattern – Steam + Decongestant",
frozenset(["weakness","dehydration"]): "Fluid deficit – ORS",
frozenset(["menstrual pain","back pain"]): "Dysmenorrhea – NSAID",
}

# ---------- 20 INTERACTIONS ----------
interaction_db = {
frozenset(["paracetamol","alcohol"]):("Moderate","Liver toxicity","Avoid alcohol"),
frozenset(["warfarin","aspirin"]):("Severe","Bleeding risk","Avoid combination"),
frozenset(["sildenafil","nitrates"]):("Severe","Severe hypotension","Contraindicated"),
frozenset(["metformin","contrast media"]):("High","Lactic acidosis","Hold 48 hrs"),
frozenset(["ibuprofen","warfarin"]):("High","Bleeding risk","Avoid"),
frozenset(["ace inhibitors","potassium"]):("Moderate","Hyperkalemia","Monitor"),
frozenset(["amoxicillin","methotrexate"]):("High","Toxicity","Avoid"),
frozenset(["statins","clarithromycin"]):("High","Rhabdomyolysis","Avoid"),
frozenset(["digoxin","verapamil"]):("Moderate","Toxicity","Monitor"),
frozenset(["benzodiazepines","alcohol"]):("Severe","Respiratory depression","Avoid"),
}

all_drugs = sorted({drug for pair in interaction_db for drug in pair})

def smart_split(text):
    return [t.strip() for t in re.split(r',|\band\b|\s+', text) if t.strip()]

def normalize_term(term, database_keys):
    if term in database_keys:
        return term
    partial = [k for k in database_keys if term in k]
    if partial:
        return partial[0]
    fuzzy = difflib.get_close_matches(term, database_keys, n=1, cutoff=0.6)
    if fuzzy:
        return fuzzy[0]
    return None

# ---------- SYMPTOM PAGE ----------
if st.session_state.page == "symptom":
    user_input = st.text_input("Type symptom (comma, space, or 'and')").lower().strip()
    if user_input:
        parts = smart_split(user_input)
        if len(parts) > 1:
            normalized = [normalize_term(p, symptom_db.keys()) for p in parts if normalize_term(p, symptom_db.keys())]
            key = frozenset(normalized[:2])
            if key in combo_db:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(combo_db[key])
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Combination not found.")
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

# ---------- INTERACTION PAGE ----------
if st.session_state.page == "interaction":
    user_input = st.text_input("Type two drugs (comma, space, or 'and')").lower().strip()
    if user_input:
        parts = smart_split(user_input)
        if len(parts) >= 2:
            d1 = normalize_term(parts[0], all_drugs)
            d2 = normalize_term(parts[1], all_drugs)
            if d1 and d2 and d1 != d2:
                key = frozenset([d1,d2])
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
                st.error("Could not identify both drugs clearly.")
        else:
            st.warning("Please enter two drug names.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
