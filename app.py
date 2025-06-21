import streamlit as st
from PIL import Image
import datetime
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

# --- STEP 1: CURRENT IMAGING ---
st.markdown("### Step 1: Upload Current Imaging")
uploaded_current = st.file_uploader(
    "Upload current radiographic images (multiple files allowed)",
    type=["jpg", "jpeg", "png", "webp", "dcm", "bmp", "tif", "tiff", "heic"],
    accept_multiple_files=True
)

# Image count
st.markdown(f"**Total files uploaded: {len(uploaded_current)}**")

today_default = datetime.date.today()
study_date = st.date_input("Date of current study:", value=today_default)

# --- STEP 2: REGION SELECTION OR FREE-FORM ---
free_form = st.checkbox("Allow free-form description without selecting anatomical regions")

regions = []
if not free_form:
    st.markdown("### Step 2: Select Regions to Analyze")
    regions = st.multiselect("Select all anatomical regions shown in the uploaded images:", [
        "Cervical Spine", "Thoracic Spine", "Lumbar Spine", "Pelvis / SI joints",
        "Hip", "Knee", "Ankle", "Foot", "Hand", "Wrist", "Elbow", "Shoulder"
    ])

# --- STEP 3: REPORT TYPE ---
mode = st.radio("Report type:", ["Single report", "Report with interval change analysis"])

# --- STEP 4: PRIOR IMAGING (if comparison selected) ---
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
                type=["jpg", "jpeg", "png", "webp", "dcm", "bmp", "tif", "tiff", "heic"],
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
if confirmed_all and 'ready' in locals() and ready:
    st.success("📝 Generating structured report...")

    findings = {}
    if free_form:
        freeform_text = st.text_area("Enter full findings (all regions or general impressions):", height=300)
    else:
        for region in regions:
            st.markdown(f"#### {region}")
            findings[region] = st.text_area(f"Enter detailed findings for {region}:", height=150)

    # Summary
    summary = st.text_area("Optional: Add a brief EMR-friendly summary (will be included separately):", height=200)

    # Build report text
    full_report = f"RheumaView™ Report\nDate of Current Study: {study_date}\n\n"
    if free_form:
        full_report += f"{freeform_text}\n"
    else:
        for region, text in findings.items():
            full_report += f"---\nRegion: {region}\n{text}\n"

    if compare_enabled and prior_images:
        full_report += "\n---\nInterval Comparison:\n"
        for label, data in prior_images.items():
            full_report += f"{label} ({data['date']}): Compared for progression/regression relative to current study.\n"

    if summary.strip():
        full_report += "\n\n=== EMR Summary ===\n" + summary.strip()

    # Create .docx
    doc = Document()
    doc.add_heading('RheumaView™ Structured Report', level=1)
    doc.add_paragraph(f"Date of Current Study: {study_date}")
    doc.add_paragraph("\n")

    for line in full_report.split("\n"):
        doc.add_paragraph(line)

    docx_filename = "rheumaview_structured_report.docx"
    doc.save(docx_filename)

    with open(docx_filename, "rb") as file:
        st.download_button(
            label="📥 Download Report (.docx)",
            data=file,
            file_name=docx_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
