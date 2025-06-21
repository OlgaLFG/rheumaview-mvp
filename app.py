import streamlit as st
from docx import Document
from PIL import Image
import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="RheumaView", page_icon=None, layout="wide")

# --- DISCLAIMER ---
st.warning("""
⚠️ **Disclaimer:**
This app does not perform automated radiologic interpretation or image recognition. Any regions listed below are for interface structure only.
The text content of this report is manually entered by the user.
Any subsequent edits made after download are not monitored or controlled by the system.
Please verify and finalize content before inserting into medical records.
Patient identifiers are not stored on any server. Reports are saved only to the user’s device.
""")

# --- LOGO ---
logo = Image.open("logo.png")
st.image(logo, width=100)

# --- HEADER ---
st.title("RheumaView")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Curated by Dr. Olga Goodman")

st.markdown("### Step 1: Upload Current Imaging")
uploaded_current = st.file_uploader(
    "Upload current radiographic images (multiple files allowed)", 
    type=["jpg", "jpeg", "png", "dcm", "webp", "bmp", "tiff"], 
    accept_multiple_files=True
)

today_default = datetime.date.today()
study_date = st.date_input("Date of current study:", value=today_default)

# --- DEMOGRAPHICS ---
st.markdown("### Step 2: Patient Demographics")
patient_name = st.text_input("Patient Name (optional)")
mrn = st.text_input("MRN / Identifier (optional)")
dob = st.text_input("Date of Birth (optional)")
age = st.number_input("Patient Age:", min_value=0, max_value=120, step=1)
sex = st.radio("Sex at Birth:", ["Female", "Male", "Other / Intersex"])
referring = st.text_input("Referring Physician (optional)")

st.markdown("### Step 3: Clinical Information")
clinical_context = st.text_area("Optional: Clinical summary (symptoms, known diagnoses, exam findings, etc.)",
                                max_chars=10000, height=150)

# --- HEADER/FOOTER ---
st.markdown("### Step 4: Report Formatting Options")
add_header_footer = st.checkbox("Include custom header and footer in final report")
custom_header = ""
custom_footer = ""
if add_header_footer:
    custom_header = st.text_area("Enter Header Text", height=60)
    custom_footer = st.text_area("Enter Footer Text", height=60)

# --- REGIONS ---
st.markdown("### Step 5: Select Regions to Analyze")
region_options = [
    "Multiple Regions (auto-assign by user)",
    "Cervical Spine", "Thoracic Spine", "Lumbar Spine", "Pelvis / SI joints",
    "Hip", "Knee", "Ankle", "Foot", "Hand", "Wrist", "Elbow", "Shoulder",
    "Other Regions (e.g., ribs, clavicle, forearm, chest, etc.)"
]
regions = st.multiselect("Select anatomical regions shown in the uploaded images:", region_options, default=["Multiple Regions (auto-assign by user)"])

mode = st.radio("Report type:", ["Single report", "Report with interval change analysis"])

compare_enabled = False
prior_images = {}
if mode == "Report with interval change analysis":
    compare_enabled = st.checkbox("Compare with prior imaging?")
    if compare_enabled:
        st.markdown("### Step 6: Upload Prior Imaging for Comparison")
        num_priors = st.number_input("How many prior studies to upload?", min_value=1, max_value=5, step=1)
        for i in range(num_priors):
            st.markdown(f"**Prior Study {i+1}:**")
            files = st.file_uploader(
                f"Upload image files for prior study #{i+1}", 
                type=["jpg", "jpeg", "png", "dcm", "webp", "bmp", "tiff"], 
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

confirmed_all = st.checkbox("I confirm that all relevant imaging has been uploaded.")

st.markdown("---")
if confirmed_all:
    ready = st.button("READY to generate report")
else:
    st.warning("Please confirm that all imaging has been uploaded before proceeding.")

if confirmed_all and ready:
    st.success("Generating structured report...")

    allow_freeform = st.checkbox("Allow free-form description without selecting anatomical regions")

    findings = {}
    if not allow_freeform:
        for region in regions:
            st.markdown(f"#### {region}")
            findings[region] = st.text_area(f"Enter detailed findings for {region}:", height=150)
    else:
        freeform_text = st.text_area("Enter full findings (all regions or general impressions):", height=250)
        findings["General"] = freeform_text

    summary = st.text_area("Optional: Add a brief EMR-friendly summary (will be included separately):", height=200)

    doc = Document()
    if add_header_footer and custom_header:
        doc.sections[0].header.paragraphs[0].text = custom_header
    doc.add_heading("RheumaView Structured Report", 0)
    doc.add_paragraph(f"Date of Current Study: {study_date}")
    doc.add_paragraph(f"Patient Name: {patient_name}")
    doc.add_paragraph(f"MRN: {mrn}")
    doc.add_paragraph(f"Date of Birth: {dob}")
    doc.add_paragraph(f"Age: {age}")
    doc.add_paragraph(f"Sex at Birth: {sex}")
    doc.add_paragraph(f"Referring Physician: {referring}")
    if clinical_context:
        doc.add_paragraph("Clinical Summary:")
        doc.add_paragraph(clinical_context)

    doc.add_heading("RheumaView Report", level=1)
    for region, text in findings.items():
        doc.add_heading(f"{region}", level=2)
        doc.add_paragraph(text)

    if compare_enabled and prior_images:
        doc.add_heading("Interval Comparison", level=2)
        for label, data in prior_images.items():
            doc.add_paragraph(f"{label} ({data['date']}): Compared for progression/regression relative to current study.")

    if summary.strip():
        doc.add_paragraph("")
        doc.add_paragraph("=== EMR Summary ===")
        doc.add_paragraph(summary.strip())

    if add_header_footer and custom_footer:
        doc.sections[0].footer.paragraphs[0].text = custom_footer

    filename = f"rheumaview_{study_date}_{sex[0]}_{age}.docx"
    doc.save(filename)

    with open(filename, "rb") as file:
        st.download_button(
            label="Download Word Report",
            data=file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
