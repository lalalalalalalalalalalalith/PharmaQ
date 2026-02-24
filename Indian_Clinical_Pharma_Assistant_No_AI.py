
import streamlit as st

st.set_page_config(page_title="Indian Clinical Pharma Assistant", layout="centered")

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    '''
    <style>
    body {
        background-color: #f4f9ff;
    }
    .main {
        background-image: linear-gradient(to bottom right, #e6f2ff, #ffffff);
    }
    footer {visibility: hidden;}
    </style>
    ''',
    unsafe_allow_html=True
)

st.title("💊 Indian Clinical Pharma Assistant")

# -----------------------------
# Symptom → OTC Database (Indian Context)
# -----------------------------

symptom_database = {

    ("fever",): {
        "drug": "Paracetamol",
        "adult": "500–650 mg every 6 hours (max 4g/day)",
        "child": "10–15 mg/kg every 6 hours",
        "form": "Tablet / Syrup",
        "notes": "If fever >3 days, test for dengue, malaria, typhoid."
    },

    ("fever", "chills"): {
        "drug": "Paracetamol + Medical evaluation",
        "adult": "650 mg every 6 hours",
        "child": "10–15 mg/kg",
        "form": "Tablet / Syrup",
        "notes": "Consider malaria or viral infection."
    },

    ("cold",): {
        "drug": "Cetirizine",
        "adult": "10 mg once daily",
        "child": "5 mg once daily",
        "form": "Tablet / Syrup",
        "notes": "Steam inhalation recommended."
    },

    ("cold", "cough"): {
        "drug": "Cetirizine + Dextromethorphan",
        "adult": "As per label dosing",
        "child": "Pediatric syrup dose",
        "form": "Tablet / Syrup",
        "notes": "If cough >2 weeks, evaluate for TB."
    },

    ("acidity",): {
        "drug": "Pantoprazole / Antacid",
        "adult": "40 mg once daily before food",
        "child": "Consult pediatric dose",
        "form": "Tablet",
        "notes": "Avoid spicy/oily food."
    },

    ("gas", "bloating"): {
        "drug": "Simethicone",
        "adult": "40–80 mg after meals",
        "child": "As per pediatric advice",
        "form": "Tablet / Drops",
        "notes": "Diet modification required."
    },

    ("diarrhea",): {
        "drug": "ORS + Zinc",
        "adult": "ORS after each loose stool",
        "child": "Zinc 10–20 mg/day for 14 days",
        "form": "ORS Powder / Tablet",
        "notes": "Watch for dehydration."
    },

    ("headache",): {
        "drug": "Ibuprofen",
        "adult": "400 mg every 8 hours",
        "child": "10 mg/kg",
        "form": "Tablet",
        "notes": "Avoid if gastric ulcer."
    },

    ("body pain",): {
        "drug": "Paracetamol / Ibuprofen",
        "adult": "Standard dosing",
        "child": "Weight based",
        "form": "Tablet",
        "notes": "Persistent pain needs evaluation."
    },

    ("allergy", "itching"): {
        "drug": "Levocetirizine",
        "adult": "5 mg once daily",
        "child": "2.5 mg once daily",
        "form": "Tablet / Syrup",
        "notes": "Avoid allergen exposure."
    },

    ("vomiting",): {
        "drug": "Ondansetron",
        "adult": "4 mg every 8 hours",
        "child": "0.15 mg/kg",
        "form": "Tablet / ODT",
        "notes": "Hydration essential."
    }

}

# -----------------------------
# Drug Interaction Database
# -----------------------------

drug_interactions = {

    ("warfarin", "aspirin"): ("Severe", "High bleeding risk"),
    ("warfarin", "ibuprofen"): ("High", "Bleeding risk"),
    ("paracetamol", "alcohol"): ("High", "Liver toxicity"),
    ("metformin", "contrast dye"): ("High", "Risk of lactic acidosis"),
    ("rifampicin", "oral contraceptive"): ("Moderate", "Reduced contraceptive efficacy"),
    ("fluoxetine", "tramadol"): ("High", "Serotonin syndrome"),
    ("insulin", "propranolol"): ("Moderate", "Masks hypoglycemia"),
    ("sildenafil", "nitroglycerin"): ("Severe", "Severe hypotension"),
    ("spironolactone", "enalapril"): ("High", "Hyperkalemia"),
    ("atorvastatin", "clarithromycin"): ("Moderate", "Myopathy risk")
}

# -----------------------------
# Symptom Section
# -----------------------------

st.header("🤖 Symptom → OTC Suggestion")
st.caption("Example: fever | cold, cough | diarrhea | allergy, itching")

symptoms_input = st.text_input("Enter symptoms separated by comma").lower()

if st.button("Get Suggestion"):
    user_symptoms = tuple(sorted([s.strip() for s in symptoms_input.split(",")]))
    found = False

    for key in symptom_database:
        if set(key).issubset(set(user_symptoms)):
            data = symptom_database[key]
            st.success(f"Suggested Drug: {data['drug']}")
            st.write(f"Adult Dose: {data['adult']}")
            st.write(f"Child Dose: {data['child']}")
            st.write(f"Dosage Form: {data['form']}")
            st.info(f"Clinical Note: {data['notes']}")
            found = True
            break

    if not found:
        st.warning("No direct match found. Seek medical evaluation.")

st.divider()

# -----------------------------
# Drug Interaction Checker
# -----------------------------

st.header("🔎 Drug Interaction Checker")

drug1 = st.text_input("Enter First Drug").lower()
drug2 = st.text_input("Enter Second Drug").lower()

if st.button("Check Interaction"):
    if (drug1, drug2) in drug_interactions:
        severity, message = drug_interactions[(drug1, drug2)]
        st.error(f"Severity: {severity}")
        st.write(f"Interaction: {message}")
    elif (drug2, drug1) in drug_interactions:
        severity, message = drug_interactions[(drug2, drug1)]
        st.error(f"Severity: {severity}")
        st.write(f"Interaction: {message}")
    else:
        st.success("No major interaction found in database.")

# -----------------------------
# Footer
# -----------------------------

st.markdown(
    "<div style='text-align: right; font-weight: bold;'>By Lalith</div>",
    unsafe_allow_html=True
)
