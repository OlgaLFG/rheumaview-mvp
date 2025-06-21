import streamlit as st
from fpdf import FPDF
from PIL import Image
import datetime
import io
import base64
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="RheumaView", page_icon=":green_square:", layout="wide")

# --- LOGO ---
logo = Image.open("logo.png")
st.image(logo, width=100)

# --- HEADER ---
st.title("🟩 RheumaView™")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Curated by Dr. Olga Goodman")

# --- IMAGE UPLOAD ---
if "current_images" not in st.session_state:
    st.session_state["current_images"] = []

st.markdown("### Step 1: Upload Current Imaging")
new_images = st.file_uploader(
    "Upload current radiographic images (add one or multiple; cumulative supported)", 
    type=["jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "heic", "dcm"], 
    accept_multiple_files=True
)

if new_images:
    st.session_state["current_images"].extend(new_images)

st.markdown(f"**Total files uploaded:** {len(st.session_state['current_images'])}")

# --- STUDY DATE ---
today_default = datetime.date.today()
study_date = st.date_input("Date of current study:", value=today_default)

# --- REGION SELECTION ---
free_form = st.checkbox("Allow free-form description without selecting anatomical regions")

regions = []
if not free_form:
    regions = st.multiselect("Select all anatomical regions shown in the uploaded images:", [
        "Cervical Spine", "Thoracic Spine", "Lumbar Spine", "Pelvis / SI joints",
        "Hip", "Knee", "Ankle", "Foot", "Hand", "Wrist", "Elbow", "Shoulder"
    ])

# --- REPORT TYPE ---
mode = st.radio("Report type:", ["Single report", "Report with interval change analysis"])

# --- PRIOR IMAGES ---
compare_enabled = False
prior_images = {}
if mode == "Report with interval change analysis":
    compare_enabled = st.checkbox("Compare with prior imaging?")
    if compare_enabled:
        st.markdown("### Step 2: Upload Prior Imaging for Comparison")
        num_priors = st.number_input("How many prior studies to upload?", min_value=1, max_value=5, step=1)
        for i in range(num_priors):
            st.markdown(f"**Prior Study {i+1}:**")
            files = st.file_uploader(
                f"Upload image files for prior study #{i+1}", 
                type=["jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "heic", "dcm"], 
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

# --- READY BUTTON ---
st.markdown("---")
ready = False
if confirmed_all:
    ready = st.button("✅ READY to generate report")
else:
    st.warning("Please confirm that all imaging has been uploaded before proceeding.")

# --- REPORT GENERATION ---
if confirmed_all and ready:
    st.success("📝 Generating structured report...")

    if free_form:
        general_findings = st.text_area("Enter general radiologic findings:", height=300)
        findings = {"General Findings": general_findings}
    else:
        findings = {}
        for region in regions:
            st.markdown(f"#### {region}")
            findings[region] = st.text_area(f"Enter detailed findings for {region}:", height=150)

    summary = st.text_area("Optional: Add a brief EMR-friendly summary:", height=200)

    # --- FORMAT SELECTION ---
    export_format = st.radio("Select report export format:", ["PDF", "Copyable text", "Download .docx"])

    full_report = f"RheumaView™ Report\nDate of Current Study: {study_date}\n\n"
    full_report += f"Uploaded files: {[f.name for f in st.session_state['current_images']]}\n\n"

    for region, text in findings.items():
        full_report += f"---\nRegion: {region}\n{text}\n"

    if compare_enabled and prior_images:
        full_report += "\n---\nInterval Comparison:\n"
        for label, data in prior_images.items():
            full_report += f"{label} ({data['date']}): Compared with current study.\n"

    if summary.strip():
        full_report += "\n\n=== EMR Summary ===\n" + summary.strip()

    # --- OUTPUT OPTIONS ---
    if export_format == "PDF":
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
        for line in full_report.split("\n"):
            pdf.multi_cell(0, 10, line)
        pdf.output("rheumaview_structured_report.pdf")

        with open("rheumaview_structured_report.pdf", "rb") as file:
            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="rheumaview_structured_report.pdf",
                mime="application/pdf"
            )

    elif export_format == "Download .docx":
        doc = Document()
        doc.add_heading("RheumaView™ Report", level=1)
        doc.add_paragraph(f"Date of Current Study: {study_date}")
        doc.add_paragraph(f"Uploaded files: {[f.name for f in st.session_state['current_images']]}")
        for region, text in findings.items():
            doc.add_heading(region, level=2)
            doc.add_paragraph(text)
        if compare_enabled and prior_images:
            doc.add_heading("Interval Comparison", level=2)
            for label, data in prior_images.items():
                doc.add_paragraph(f"{label} ({data['date']}): Compared with current study.")
        if summary.strip():
            doc.add_heading("EMR Summary", level=2)
            doc.add_paragraph(summary.strip())
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="📝 Download Word Document",
            data=buffer,
            file_name="rheumaview_structured_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    else:
        st.markdown("### 📋 Copyable Text Output")
        st.text_area("Copy this report:", full_report, height=500)

