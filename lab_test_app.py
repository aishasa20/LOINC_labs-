import streamlit as st
import pandas as pd

# ---- Load and cache data ----
@st.cache_data
def load_data():
    df = pd.read_csv("lab_tests_US.csv")
    return df

df = load_data()

class_to_group = {
    'ALLERGY': 'Allergy',
    'BLDBK': 'Blood Bank',
    'CELLMARK': 'Cell Markers',
    'CHAL': 'Challenge Tests',
    'CHAL.ROUTINE': 'Routine Challenge Tests',
    'CHEM': 'Chemistry',
    'COAG': 'Coagulation',
    'DRUG/TOX': 'Toxicology',
    'FERT': 'Fertility',
    'HEM/BC': 'CBC & Hematology',
    'MICRO': 'Microbiology',
    'MOLPATH': 'Molecular Pathology',
    'MOLPATH.PHARMG': 'Pharmacogenomics',
    'PANEL.CHEM': 'Chemistry Panels',
    'PANEL.HEM/BC': 'CBC Panels',
    'PANEL.MICRO': 'Microbiology Panels',
    'PANEL.SERO': 'Serology Panels',
    'PANEL.UA': 'Urinalysis Panels',
    'PATH': 'Pathology',
    'SERO': 'Serology',
    'UA': 'Urinalysis',
    'LABORDERS': 'Lab Orders',
    'MISC': 'Miscellaneous',
    'CHAL': 'Challenge Tests',
    'CHAL.ROUTINE': 'Routine Challenge Tests',
}

# Apply mapping
df['Category'] = df['CLASS'].map(class_to_group).fillna('Other')

# ---- Page Setup ----
st.set_page_config(page_title="Lab Test", layout="wide")
st.title("Search Lab Test")

# ---- Sidebar Filters ----
with st.sidebar:
    st.markdown("### 🔍 Filter Lab Tests")

    category_options = sorted(df['Category'].unique())
    selected_category = st.sidebar.selectbox("Test Category", ["All"] + category_options)


    specimen_types = sorted(df['SYSTEM'].dropna().unique())
    selected_specimen = st.selectbox("Specimen Type", ["All"] + specimen_types)

# ---- Main Search and Results ----
search_term = st.text_input("Search Lab Test", placeholder="Type 'CBC', 'glucose', 'hemoglobin'...")

# Filter dataset
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_specimen != "All":
    filtered_df = filtered_df[filtered_df["SYSTEM"] == selected_specimen]

if search_term:
    filtered_df = filtered_df[
        filtered_df["LONG_COMMON_NAME"].str.contains(search_term, case=False, na=False)
    ]

if search_term:
    filtered_df = filtered_df[
        filtered_df["SHORTNAME"].str.contains(search_term, case=False, na=False)
    ]

if search_term: 
    filtered_df = filtered_df[
        filtered_df["COMPONENT"].str.contains(search_term, case=False, na=False)
    ]

# Rename columns
display_df = filtered_df.rename(columns={
    'LOINC_NUM': 'LOINC Code',
    "SHORTNAME": "Short Name",
    'LONG_COMMON_NAME': 'Long Name',
    'SYSTEM': 'Specimen',
    'COMPONENT': 'Component',
    'PROPERTY': 'Property',
    'SCALE_TYP': 'Scale',
    'METHOD_TYP': 'Method',  
})

# Select columns to show
columns_to_show = [
    'LOINC Code', 'Short Name', 'Long Name',
    'Specimen', 'Component', 'Category', 'Property', 'Scale', 'Method'
]

st.markdown(f"### Results ({len(display_df)} test{'s' if len(display_df) != 1 else ''} found):")
st.dataframe(display_df[columns_to_show], use_container_width=True)

# ---- Explanation Section ----
with st.expander("ℹ️ Column Definitions & Specimen Abbreviations"):
    st.markdown("""
### 📘 Column Definitions
- **LOINC Code**: Unique identifier assigned to the lab test
- **Short Name**: Abbreviated test name (used in some systems)
- **Long Name**: Full descriptive name of the test
- **Specimen**: Sample type used for the test (e.g. Blood, Urine)
- **Component**: What is being measured (e.g. Hemoglobin, Glucose)
- **Property**: What property is being measured (e.g. concentration, mass)
- **Scale**: Type of result (e.g. Quantitative, Ordinal)
- **Method**: Specific lab method if defined (e.g. HPLC, Immunoassay)

### 🧬 Common Specimen Abbreviations
| Abbreviation | Meaning                  |
|--------------|---------------------------|
| Bld          | Blood                     |
| Ser          | Serum                     |
| Plas         | Plasma                    |
| Urine        | Urine                     |
| CSF          | Cerebrospinal Fluid       |
| Saliva       | Saliva                    |
| Stool        | Stool (Feces)             |
| Swab         | Swab from site (e.g. throat, wound) |
| Bone Marrow  | Bone Marrow aspirate      |

    """)



