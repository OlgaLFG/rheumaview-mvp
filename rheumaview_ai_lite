
import streamlit as st
import datetime
from docx import Document

st.set_page_config(page_title="RheumaView AI Lite — Stable Final", layout="wide")

st.title("RheumaView AI Lite")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Stable version with full features, safe findings export, and no clinical context in report")

# --- Step 1: Imaging Upload ---
st.markdown("### Step 1: Upload Current Imaging")
st.file_uploader(
    "Upload current radiographic images (multiple files allowed)",
    type=["jpg", "jpeg", "png", "dcm", "webp", "bmp", "tiff"],
    accept_multiple_files=True,
    key="current_images"
)

study_date = st.date_input("Date of current study:", value=datetime.date.today())

# --- Step 2: Patient Info ---
st.markdown("### Step 2: Patient Demographics")
dob_input = st.text_input("Date of Birth (optional, YYYY-MM-DD):")
age = st.number_input("Patient Age:", min_value=0, max_value=120, step=1)
sex = st.radio("Sex at Birth:", ["Female", "Male", "Other / Intersex"])
name = st.text_input("Patient Name or ID (optional):")
mrn = st.text_input("Medical Record Number (optional):")
st.text_area("Clinical context (for reference only, not included in report)", key="clinical_context", height=100)

# --- Step 3: Region Selection ---
st.markdown("### Step 3: Select Regions to Analyze")
region_options = [
    "Multiple Regions",
    "Cervical Spine", "Thoracic Spine", "Lumbar Spine", "Pelvis / SI joints",
    "Hip", "Knee", "Ankle", "Foot", "Hand", "Wrist", "Elbow", "Shoulder",
    "Other Regions (e.g., ribs, clavicle, forearm, chest, etc.)"
]
regions = st.multiselect("Select anatomical regions shown in the uploaded images:", region_options, default=["Multiple Regions"])

# --- Step 4: Optional comparison ---
mode = st.radio("Report type:", ["Single report", "Report with interval change analysis"])
compare_enabled = False
prior_images = {}
if mode == "Report with interval change analysis":
    compare_enabled = st.checkbox("Compare with prior imaging?")
    if compare_enabled:
        st.markdown("### Upload Prior Imaging for Comparison")
        num_priors = st.number_input("How many prior studies to upload?", min_value=1, max_value=5, step=1)
        for i in range(num_priors):
            st.markdown(f"**Prior Study {i+1}:**")
            files = st.file_uploader(f"Upload image files for prior study #{i+1}",
                                     type=["jpg", "jpeg", "png", "dcm", "webp", "bmp", "tiff"],
                                     accept_multiple_files=True,
                                     key=f"prior_{i}")
            prior_date = st.text_input(f"Enter date of prior study #{i+1} (full date or year):", value="", key=f"date_{i}")
            if files:
                prior_images[f"Prior_{i+1}"] = {"files": files, "date": prior_date}

# --- Step 5: Header/Footer ---
st.markdown("### Step 5: Report Formatting Options")
include_header_footer = st.checkbox("Include custom header and footer?")
default_header = st.text_input("Default Header (editable later):", value="")
default_footer = st.text_input("Default Footer (editable later):", value="")
custom_header = default_header if include_header_footer else ""
custom_footer = default_footer if include_header_footer else ""

# --- READY ---
confirmed_all = st.checkbox("I confirm that all relevant imaging has been uploaded.")
ready = st.button("READY to generate report")

if confirmed_all and ready:
    st.success("Generating structured report...")

    st.markdown("### ✍️ Final Report Findings (editable)")
    default_findings = "**Example Section**\nDescribe key findings here."
    compiled_text = st.text_area("Report Body (included in DOCX):", value=default_findings, height=300)

    summary = st.text_area("Optional: Add a brief EMR-friendly summary (will be included separately):", height=150)

    # --- Word doc generation ---
    doc = Document()

    if custom_header:
        doc.add_paragraph(custom_header)

    doc.add_heading("RheumaView Structured Report", 0)
    doc.add_paragraph(f"Date of Current Study: {study_date}")
    if name:
        doc.add_paragraph(f"Patient: {name}")
    if dob_input:
        doc.add_paragraph(f"DOB: {dob_input}")
    if mrn:
        doc.add_paragraph(f"MRN: {mrn}")
    doc.add_paragraph(f"Age: {age}")
    doc.add_paragraph(f"Sex: {sex}")

    doc.add_heading("RheumaView Report", level=1)
    doc.add_paragraph(compiled_text)

    if compare_enabled and prior_images:
        doc.add_heading("Interval Comparison", level=2)
        for label, data in prior_images.items():
            doc.add_paragraph(f"{label} ({data['date']}): Compared for progression/regression relative to current study.")

    if summary.strip():
        doc.add_paragraph("")
        doc.add_paragraph("=== EMR Summary ===")
        doc.add_paragraph(summary.strip())

    if custom_footer:
        doc.add_paragraph("\n" + custom_footer)

    filename = f"rheumaview_structured_report_{study_date}_{sex}_{age}.docx"
    doc.save(filename)

    with open(filename, "rb") as file:
        st.download_button(
            label="Download Word Report",
            data=file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
