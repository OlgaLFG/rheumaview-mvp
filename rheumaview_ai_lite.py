
import streamlit as st
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="RheumaView AI Lite", layout="wide")

# --- HEADER ---
st.title("RheumaView AI Lite")
st.subheader("Semi-Automated Radiograph Reporting Interface")
st.caption("Curated by Dr. Olga Goodman")

# --- STUDY DATA ---
today_default = datetime.date.today()
study_date = st.date_input("Date of current study:", value=today_default)
age = st.number_input("Patient Age:", min_value=0, max_value=120, step=1, value=50)
sex = st.radio("Sex at Birth:", ["Female", "Male", "Other / Intersex"])
regions = st.multiselect("Select regions to analyze:", [
    "Multiple Regions", "SI Joints", "Spine (DISH)", "Peripheral Joints"
], default=["Multiple Regions"])

st.markdown("---")

# --- Expand logic ---
if "Multiple Regions" in regions:
    expanded_regions = ["SI Joints", "Spine (DISH)", "Peripheral Joints"]
else:
    expanded_regions = regions

# --- AI SUGGESTION BLOCKS ---

if "SI Joints" in expanded_regions:
    st.header("Sacroiliac Joints (SI)")
    si_level = st.radio("Confidence level (SI):", ["Low", "Moderate", "High"], key="si_level")
    if si_level == "Low":
        st.text_area("AI-style phrasing:", 
            "Sacroiliac joints are symmetric. Mild subchondral sclerosis without erosions or joint space narrowing. "
            "Findings may represent early sacroiliitis or degenerative change.", height=150, key="si_text_low")
    elif si_level == "Moderate":
        st.text_area("AI-style phrasing:", 
            "Mild irregularity and sclerosis of bilateral sacroiliac joints, more pronounced on iliac sides. "
            "No erosions or ankylosis. Findings suggest early sacroiliitis.", height=150, key="si_text_moderate")
    else:
        st.text_area("AI-style phrasing:", 
            "Bilateral sacroiliac joint sclerosis, erosions, and joint space narrowing. "
            "Findings consistent with Grade II–III sacroiliitis.", height=150, key="si_text_high")

if "Spine (DISH)" in expanded_regions:
    st.header("Spinal Findings (DISH)")
    dish_level = st.radio("Confidence level (DISH):", ["Moderate", "High"], key="dish_level")
    if dish_level == "Moderate":
        st.text_area("AI-style phrasing:", 
            "Anterior vertebral body osteophytes and subtle ossification along the anterior longitudinal ligament "
            "at T12–L2, with preserved disc spaces. Findings may be consistent with early DISH.", height=150, key="dish_text_mod")
    else:
        st.text_area("AI-style phrasing:", 
            "Flowing ossification along the anterior longitudinal ligament spanning T12 to L3 with preserved disc "
            "heights and absence of significant degenerative change. Findings consistent with diffuse idiopathic "
            "skeletal hyperostosis (DISH).", height=150, key="dish_text_high")

if "Peripheral Joints" in expanded_regions:
    st.header("Peripheral Joints")
    st.markdown("##### SUGGESTED REPORTING TEMPLATE (Plain Radiograph)")
    joint_space = st.text_input("Joint space narrowing (symmetry + location):")
    erosions = st.text_input("Erosions (present/absent, location, character):")
    density = st.selectbox("Bone density:", ["Normal", "Juxta-articular osteopenia"])
    periosteal = st.selectbox("Periosteal reaction:", ["Absent", "Present"])
    soft_tissue = st.text_input("Soft tissue (swelling, masses, calcifications):")
    osteophytes = st.selectbox("Osteophytes:", ["None", "Mild", "Moderate", "Severe"])
    other = st.text_input("Other findings (ankylosis, subluxation, etc.):")
    impression = st.text_area("Impression:",
        "Imaging features are [ / are not ] consistent with an inflammatory arthropathy.\n"
        "The findings may suggest [RA / PsA / gout / EOA / OA], based on [key features].", height=150)
