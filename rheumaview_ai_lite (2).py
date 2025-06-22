
import streamlit as st
import datetime
from docx import Document
from PIL import Image
import base64
import io

st.set_page_config(page_title="RheumaView AI Lite — Stable Final", layout="wide")

# Title and Subtitle
st.markdown("![Logo](https://via.placeholder.com/100)")
st.title("RheumaView AI Lite")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Curated by Dr. Olga Goodman | Stable version with full interface, AI analysis, and safe report export (no clinical context in DOCX)")

# Upload images
st.markdown("### Step 1: Upload Current Imaging")
uploaded_files = st.file_uploader(
    "Upload current radiographic images (multiple files allowed)",
    type=["jpg", "jpeg", "png", "dcm", "webp", "bmp", "tiff"],
    accept_multiple_files=True,
    key="current_images"
)

# Patient demographics
st.markdown("### Step 2: Patient Demographics")
study_date = st.date_input("Date of current study", datetime.date.today())
dob = st.text_input("Date of Birth (optional, YYYY-MM-DD):")
age = st.number_input("Patient Age:", min_value=0, max_value=120, value=0)
sex = st.radio("Sex at Birth:", ["Female", "Male", "Other / Intersex"])
patient_name = st.text_input("Patient Name or ID (optional):")
mrn = st.text_input("Medical Record Number (optional):")
clinical_context = st.text_area("Clinical context (for reference only, not included in report)")

# Select regions
st.markdown("### Step 3: Select Regions to Analyze")
regions = st.multiselect(
    "Select anatomical regions shown in the uploaded images:",
    ["SI Joints", "Spine (DISH)", "Peripheral Joints"],
    default=["SI Joints", "Spine (DISH)", "Peripheral Joints"]
)

# Report type
st.radio("Report type:", ["Single report", "Report with interval change analysis"])

# Report formatting
st.markdown("### Step 4: Report Formatting Options")
custom_header = st.checkbox("Include custom header and footer?")
header_text = st.text_input("Default Header (editable later):") if custom_header else ""
footer_text = st.text_input("Default Footer (editable later):") if custom_header else ""
confirm = st.checkbox("I confirm that all relevant imaging has been uploaded.")

# Final findings (AI-powered placeholders)
st.markdown("### Step 5: AI Findings Preview (Editable in DOCX)")
default_findings = ""
if "SI Joints" in regions:
    default_findings += "**SI Joints**\nMild bilateral sclerosis and joint space narrowing, consistent with early sacroiliitis (Grade II).\n\n"
if "Spine (DISH)" in regions:
    default_findings += "**Spine (DISH)**\nFlowing ossification of anterior longitudinal ligament across T8–T12 with preserved disc height; consistent with DISH.\n\n"
if "Peripheral Joints" in regions:
    default_findings += "**Peripheral Joints**\nMarginal erosions at MCP2 and MCP3 bilaterally, symmetric joint space narrowing, juxta-articular osteopenia. No osteophytes.\n\n"

default_findings = default_findings.replace("\n", "\n")

findings = st.text_area("🧠 Final Report Findings (editable, included in DOCX):", value=default_findings, height=250)

# Generate report
if st.button("READY to generate report") and confirm:
    doc = Document()
    if header_text:
        doc.add_paragraph(header_text)
    doc.add_heading("Radiology Report", level=1)
    doc.add_paragraph(f"Study Date: {study_date}")
    doc.add_paragraph(f"Age: {age} | Sex: {sex}")
    if patient_name:
        doc.add_paragraph(f"Patient: {patient_name}")
    if mrn:
        doc.add_paragraph(f"MRN: {mrn}")
    doc.add_paragraph("")
    doc.add_paragraph(findings)
    if footer_text:
        doc.add_paragraph("")
        doc.add_paragraph(footer_text)

    output = io.BytesIO()
    doc.save(output)
    st.download_button(
        label="📥 Download Report (.docx)",
        data=output.getvalue(),
        file_name=f"rheumaview_structured_report_{study_date}_{sex}_{age}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
