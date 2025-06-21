import streamlit as st
from fpdf import FPDF
from PIL import Image
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="RheumaView", page_icon=":green_square:", layout="wide")

# --- LOGO ---
logo = Image.open("logo.png")
st.image(logo, width=100)

# --- HEADER ---
st.title("🟩 RheumaView™")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Curated by Dr. Olga Goodman")

# --- STEP 1: CURRENT IMAGING ---
st.markdown("### Step 1: Upload Current Imaging")
uploaded_current = st.file_uploader(
    "Upload current radiographic images (multiple files allowed)", 
    type=["jpg", "jpeg", "png", "dcm"], 
    accept_multiple_files=True
)

today_default = datetime.date.today()
study_date = st.date_input("Date of current study:", value=today_default)

# --- STEP 2: REGION SELECTION ---
st.markdown("### Step 2: Select Regions to Analyze")
regions = st.multiselect("Select all anatomical regions shown in the uploaded images:", [
    "Cervical Spine", "Thoracic Spine", "Lumbar Spine", "Pelvis / SI joints",
    "Hip", "Knee", "Ankle", "Foot", "Hand", "Wrist", "Elbow", "Shoulder"
])

# --- STEP 3: REPORT MODE ---
mode = st.radio("Report type:", ["Single report", "Report with interval change analysis"])

compare_enabled = False
prior_images = {}

if mode == "Report with interval change analysis":
    compare_enabled = st.checkbox("Compare with prior imaging?")
    if compare_enabled:
        st.markdown("### Step 3: Upload Prior Imaging for Comparison")
        num_priors = st.number_input("How many prior studies to upload?", min_value=1, max_value=5, step=1)
        for i in range(num_priors):
            st.markdown(f"**Prior Study {i+1}:**")
            files = st.file_uploader(
                f"Upload image files for prior study #{i+1}", 
                type=["jpg", "jpeg", "png", "dcm"], 
                accept_multiple_files=True, 
                key=f"prior_{i}"
            )
            prior_date = st.text_input(
                f"Enter date of prior study #{i+1} (full date or year):", 
                value="", 
                key=f"date_{i}"
            )
            if files:
                prior_images[f"Prior_{i+1}"] = {"files": files, "date": prior_date}

# --- CONFIRMATION ---
confirmed_all = st.checkbox("I confirm that all relevant imaging has been uploaded.")

st.markdown("---")
if confirmed_all:
    ready = st.button("✅ READY to generate report")
else:
    st.warning("Please confirm that all imaging has been uploaded before proceeding.")

# --- REPORT GENERATION ---
if confirmed_all and ready:
    st.success("📝 Generating structured report...")

    findings = {}
    for region in regions:
        st.markdown(f"#### {region}")
        findings[region] = st.text_area(f"Enter detailed findings for {region}:", height=150)

    # --- OPTIONAL EMR SUMMARY ---
    summary = st.text_area("Optional: Add a brief EMR-friendly summary (will be included separately):", height=200)

    # --- COMPOSE REPORT TEXT ---
    full_report = f"RheumaView™ Report\nDate of Current Study: {study_date}\n\n"
    for region, text in findings.items():
        full_report += f"---\nRegion: {region}\n{text}\n"

    if compare_enabled and prior_images:
        full_report += "\n---\nInterval Comparison:\n"
        for label, data in prior_images.items():
            full_report += f"{label} ({data['date']}): Compared for progression/regression relative to current study.\n"

    if summary.strip():
        full_report += "\n\n=== EMR Summary ===\n" + summary.strip()

    # --- PDF EXPORT ---
    pdf = FPDF()
    pdf.add_page()

    # Register DejaVu font for Unicode support
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in full_report.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output("rheumaview_structured_report.pdf")

    with open("rheumaview_structured_report.pdf", "rb") as file:
        st.download_button(
            label="📄 Download Full PDF Report",
            data=file,
            file_name="rheumaview_structured_report.pdf",
            mime="application/pdf"
        )
