import streamlit as st
from docx import Document

# --- CONFIGURATION ---
st.set_page_config(page_title="RheumaView AI Lite", layout="wide")
st.title("RheumaView AI Lite")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("AI analysis disabled. Protected against rerun crashes.")

# --- Step 1: Upload Images ---
uploaded_images = st.file_uploader(
    "Step 1: Upload current imaging",
    type=["jpg", "jpeg", "png", "webp", "dcm", "bmp", "tiff"],
    accept_multiple_files=True,
    key="img"
)

# --- Step 2: Demographics ---
st.markdown("### Step 2: Patient Demographics")
st.text_input("Date of Birth (YYYY-MM-DD)", key="dob")
st.text_input("Patient Age", key="age")
st.selectbox("Sex at Birth", ["", "Female", "Male", "Other"], key="sex")
st.text_input("Patient Name or ID", key="name")
st.text_input("MRN", key="mrn")
st.text_area("Clinical context (not included in report)", key="clinical_context")

# --- Step 3: Region ---
st.markdown("### Step 3: Region")
st.selectbox("Anatomical region(s)", [
    "Multiple Regions", "Cervical Spine", "Thoracic Spine", "Lumbar Spine",
    "Pelvis/SI/Sacrum", "Hips", "Knees", "Feet", "Hands", "Shoulders"
], key="region")

# --- Step 4: Header/Footer ---
st.text_input("Header (optional)", value="RheumaView", key="header")
st.text_input("Footer (optional)", value="Curated by Dr. Olga Goodman", key="footer")

# --- Step 5: READY ---
st.markdown("### Step 5: Confirm")
ready = st.checkbox("READY – I have completed data entry")

# --- Step 6: Generate Report ---
if st.button("Generate Report"):
    if not ready:
        st.warning("Please confirm readiness by checking the READY box.")
    elif not st.session_state.img:
        st.warning("Please upload at least one image.")
    else:
        try:
            doc = Document()
            doc.add_heading("RheumaView Structured Radiology Report", 0)
            doc.add_paragraph(f"Patient: {st.session_state.name or 'N/A'}")
            doc.add_paragraph(f"Age: {st.session_state.age or 'N/A'}     Sex: {st.session_state.sex or 'N/A'}")
            if st.session_state.dob:
                doc.add_paragraph(f"Date of Birth: {st.session_state.dob}")
            if st.session_state.mrn:
                doc.add_paragraph(f"MRN: {st.session_state.mrn}")
            doc.add_paragraph(f"Region analyzed: {st.session_state.region}")
            doc.add_paragraph(" ")
            doc.add_paragraph("Findings:")
            doc.add_paragraph("This is a placeholder body. AI is not active in this version.")
            doc.add_paragraph(" ")
            doc.add_paragraph("---")
            doc.add_paragraph(st.session_state.header)
            doc.add_paragraph(st.session_state.footer)

            output_path = "/mnt/data/rheumaview_structured_report_final.docx"
            doc.save(output_path)

            st.success("✅ Report ready.")
            with open(output_path, "rb") as f:
                st.download_button("Download Report", f, file_name="rheumaview_structured_report.docx")

        except Exception as e:
            st.error("❌ Error creating report.")
