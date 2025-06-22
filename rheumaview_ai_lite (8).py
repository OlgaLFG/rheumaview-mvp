
import streamlit as st
from docx import Document
from datetime import datetime
import os

st.set_page_config(page_title="RheumaView™", layout="wide")

st.markdown("## 🟩 RheumaView™")
st.markdown("**Radiologic Reasoning for Rheumatologists**  
_Curated by Dr. Olga Goodman_")
st.markdown("---")

st.markdown("⚠️ *This app does not perform automated radiologic interpretation or image recognition. All reports are user-generated. No PHI is stored. All data will be deleted after 30 minutes of inactivity or upon user confirmation.*")

# Step 1: Upload Current Images
st.markdown("### Step 1: Upload Current Imaging")
uploaded_files = st.file_uploader("Upload current radiographic images (multiple files allowed)",
                                  type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "dcm"],
                                  accept_multiple_files=True)

study_date = st.date_input("Date of current study:", value=datetime.today())

# Step 2: Demographics
st.markdown("### Step 2: Patient Demographics")
dob = st.text_input("Date of Birth (optional, YYYY-MM-DD):")
age = ""
if dob:
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        age = int((datetime.today() - dob_date).days / 365.25)
    except:
        st.warning("Invalid date format.")
st.text_input("Patient Age:", value=age if age else "", disabled=True)
sex = st.radio("Sex at Birth:", options=["Female", "Male", "Other / Intersex"])
name = st.text_input("Patient Name or ID (optional):")
mrn = st.text_input("Medical Record Number (optional):")

# Step 3: Report Type
st.markdown("### Step 3: Select Report Type")
report_type = st.radio("Report type:", ["Single report", "Report with interval change analysis"])

# Step 4: Prior Studies
prior_count = 0
if report_type == "Report with interval change analysis":
    prior_count = st.number_input("How many prior studies to upload?", min_value=1, max_value=5, step=1)
    prior_studies = []
    for i in range(prior_count):
        st.markdown(f"#### Prior Study {i+1}")
        prior_files = st.file_uploader(f"Upload images for prior study #{i+1}",
                                       type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "dcm"],
                                       accept_multiple_files=True, key=f"prior_{i}")
        prior_date = st.text_input(f"Enter date of prior study #{i+1} (YYYY-MM-DD or YYYY):", key=f"date_{i}")
        prior_studies.append((prior_files, prior_date))

# Step 5: Interpretation Trigger
st.markdown("### Step 5: READY to Generate Report?")
ready_flag = st.text_input("Type 'READY' to begin interpretation:")

# Step 6: Generate Report
if ready_flag.strip().upper() == "READY":
    st.success("READY flag received. Generating report...")

    # Report Generation
    doc = Document()
    doc.add_heading("RheumaView™ Radiology Report", 0)
    doc.add_paragraph(f"Study Date: {study_date}")
    if age:
        doc.add_paragraph(f"Patient Age: {age}")
    doc.add_paragraph(f"Sex at Birth: {sex}")
    if name:
        doc.add_paragraph(f"Name/ID: {name}")
    if mrn:
        doc.add_paragraph(f"MRN: {mrn}")
    doc.add_paragraph("This is a placeholder for region analysis and image-based findings.")
    doc.add_paragraph("⚠️ This document is user-generated. No PHI is stored. All content reviewed manually.")

    # Save .docx
    filename = f"rheumaview_structured_report_{datetime.today().date()}_{sex}_{age or 'NA'}.docx"
    doc_path = Path("/mnt/data") / filename
    doc.save(doc_path)

    st.success("Report generated successfully.")
    with open(doc_path, "rb") as file:
        st.download_button(label="⬇️ Download Report (.docx)", data=file, file_name=filename)
else:
    st.info("Awaiting 'READY' to proceed with interpretation.")
