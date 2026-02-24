
import streamlit as st
import difflib
import re

st.set_page_config(page_title="PHARMAQ", layout="wide")

# ---------------- STYLE ----------------
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

.mild { background-color: #0f3d2e; color: #4cd137; padding: 15px; border-radius: 10px; }
.moderate { background-color: #4a3b00; color: #ffd166; padding: 15px; border-radius: 10px; }
.high { background-color: #3b1f00; color: #ff922b; padding: 15px; border-radius: 10px; }
.severe { background-color: #3b0000; color: #ff4d4d; padding: 15px; border-radius: 10px; }

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

# ---------------- PAGE SWITCH ----------------
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

# ---------------- DATA BUILDERS ----------------
def build_symptom(cause, otc):
    return {
        "Cause": cause,
        "OTC": otc,
        "Adult Dose": "As per standard adult dosing guidelines.",
        "Pediatric Dose": "Weight-based dosing where applicable.",
        "Tips": "Maintain hydration and adequate rest.",
        "Do's": "Follow proper dosing schedule.",
        "Don'ts": "Avoid overdose or duplicate therapy.",
        "When to Consult Doctor": "If symptoms persist >3 days or worsen.",
        "Red Flag": "Severe symptoms, high fever, breathing difficulty."
    }

# ---------------- 40 SYMPTOMS ----------------
symptom_data = [
("fever","Viral infection","Paracetamol"),
("cold","Viral URI","Cetirizine"),
("headache","Tension","Paracetamol"),
("body pain","Myalgia","Ibuprofen"),
("acidity","GERD","Pantoprazole"),
("diarrhea","Gastroenteritis","ORS + Zinc"),
("vomiting","Gastritis","Ondansetron"),
("cough","URI","Dextromethorphan"),
("sore throat","Pharyngitis","Lozenges"),
("gas","Dyspepsia","Simethicone"),
("dizziness","Vertigo","Meclizine"),
("allergy","Allergic rhinitis","Cetirizine"),
("back pain","Muscle strain","Ibuprofen"),
("toothache","Dental inflammation","Paracetamol"),
("ear pain","Otitis","Paracetamol"),
("eye redness","Allergy","Lubricant drops"),
("constipation","Low fiber","Isabgol"),
("burning urination","UTI suspicion","Hydration"),
("insomnia","Stress","Melatonin"),
("anxiety","Stress","Lifestyle modification"),
("joint pain","Inflammatory","Ibuprofen"),
("muscle cramps","Electrolyte imbalance","ORS"),
("dehydration","Fluid loss","ORS"),
("nasal congestion","Cold","Oxymetazoline"),
("sinus pain","Sinusitis","Steam inhalation"),
("ear blockage","Wax impaction","Ear drops"),
("mouth ulcer","Aphthous ulcer","Topical gel"),
("hair fall","Nutritional","Biotin"),
("dry skin","Dehydration","Moisturizer"),
("minor burn","Thermal injury","Silver sulfadiazine"),
("cuts","Minor injury","Antiseptic"),
("bruises","Trauma","Cold compress"),
("sunburn","UV exposure","Aloe gel"),
("weakness","Fatigue","Multivitamin"),
("menstrual pain","Dysmenorrhea","Mefenamic acid"),
("migraine","Neurovascular","Sumatriptan"),
("nausea","Gastritis","Ondansetron"),
("ulcer pain","Peptic ulcer","Pantoprazole"),
("itching","Allergy","Cetirizine"),
("rash","Dermatitis","Calamine")
]

symptom_db = {name: build_symptom(cause, otc) for name, cause, otc in symptom_data}

# ---------------- 20 COMBINATIONS ----------------
combo_pairs = [
("fever","cold"),("fever","headache"),("diarrhea","vomiting"),
("cough","cold"),("back pain","body pain"),("rash","itching"),
("gas","acidity"),("nasal congestion","sinus pain"),
("weakness","dehydration"),("menstrual pain","back pain"),
("nausea","vomiting"),("fever","body pain"),
("joint pain","muscle cramps"),("allergy","eye redness"),
("ear pain","fever"),("headache","dizziness"),
("sunburn","dry skin"),("ulcer pain","acidity"),
("cough","sore throat"),("anxiety","insomnia")
]

combo_db = {frozenset(pair): f"Combined presentation: {pair[0]} + {pair[1]} – Symptomatic treatment advised." for pair in combo_pairs}

# ---------------- 20 INTERACTIONS ----------------
interaction_entries = [
("paracetamol","alcohol","Moderate","Liver toxicity","Avoid alcohol"),
("warfarin","aspirin","Severe","Bleeding risk","Avoid combination"),
("sildenafil","nitrates","Severe","Severe hypotension","Contraindicated"),
("metformin","contrast media","High","Lactic acidosis","Hold 48 hrs"),
("ibuprofen","warfarin","High","Bleeding risk","Avoid"),
("ace inhibitors","potassium","Moderate","Hyperkalemia","Monitor potassium"),
("amoxicillin","methotrexate","High","Toxicity","Avoid"),
("statins","clarithromycin","High","Rhabdomyolysis","Avoid"),
("digoxin","verapamil","Moderate","Digoxin toxicity","Monitor"),
("benzodiazepines","alcohol","Severe","Respiratory depression","Avoid"),
("insulin","beta blockers","Moderate","Masked hypoglycemia","Monitor"),
("clopidogrel","omeprazole","Moderate","Reduced effect","Use pantoprazole"),
("rifampicin","oral contraceptives","High","Reduced efficacy","Backup contraception"),
("lithium","nsaids","High","Lithium toxicity","Monitor levels"),
("fluoxetine","tramadol","High","Serotonin syndrome","Avoid"),
("spironolactone","potassium","High","Hyperkalemia","Monitor"),
("amlodipine","simvastatin","Moderate","Increased statin level","Limit dose"),
("ciprofloxacin","theophylline","High","Toxicity","Monitor"),
("heparin","aspirin","Severe","Bleeding risk","Avoid"),
("metronidazole","alcohol","Severe","Disulfiram reaction","Avoid alcohol")
]

interaction_db = {frozenset([d1,d2]):(sev,mech,adv) for d1,d2,sev,mech,adv in interaction_entries}
all_drugs = sorted({drug for pair in interaction_db for drug in pair})

# ---------------- SMART HELPERS ----------------
def smart_split(text):
    return [t.strip() for t in re.split(r',|\band\b|\s+', text) if t.strip()]

def normalize_term(term, keys):
    if term in keys:
        return term
    partial = [k for k in keys if term in k]
    if partial:
        return partial[0]
    fuzzy = difflib.get_close_matches(term, keys, n=1, cutoff=0.6)
    if fuzzy:
        return fuzzy[0]
    return None

# ---------------- SYMPTOM PAGE ----------------
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
                for section in data:
                    with st.expander(section):
                        st.write(data[section])
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
            if d1 and d2 and d1 != d2:
                key = frozenset([d1,d2])
                if key in interaction_db:
                    sev, mech, adv = interaction_db[key]
                    st.markdown(f'<div class="{sev.lower()}">', unsafe_allow_html=True)
                    st.write(f"**Severity:** {sev}")
                    st.write(f"**Mechanism:** {mech}")
                    st.write(f"**Advice:** {adv}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="mild">No major interaction found.</div>', unsafe_allow_html=True)
            else:
                st.error("Could not identify both drugs clearly.")
        else:
            st.warning("Please enter two drug names.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
