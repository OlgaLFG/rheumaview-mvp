
import streamlit as st
from fpdf import FPDF

# --- PAGE CONFIG ---
st.set_page_config(page_title="RheumaView", page_icon=":green_square:", layout="centered")

# --- LOGO ---
st.image("logo.png", width=100)

# --- TITLE ---
st.title("🟩 RheumaView™")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Curated by Dr. Olga Goodman")

# --- MODE SELECTION ---
mode = st.radio("Choose interpretation mode:", ["Template Mode", "Manual Input (Smart Assist)"], index=0)

# --- REGION SELECT ---
region = st.selectbox("Select anatomical region:", [
    "Sacroiliac Joints",
    "Cervical Spine",
    "Lumbar Spine",
    "Hands",
    "Feet",
    "Other"
])

# --- TEXT AREA ---
if mode == "Template Mode":
    st.markdown("✏️ Please enter your structured radiology description below:")
    template_text = st.text_area("Template Text", height=200, value="")
else:
    st.markdown("🧠 Smart Assist Mode is currently in beta.")
    template_text = st.text_area("Enter findings manually:", height=200, value="")

# --- EXPORT TO PDF ---
def export_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output("rheumaview_report.pdf")

if st.button("📄 Export to PDF"):
    if template_text.strip():
        export_to_pdf(template_text)
        with open("rheumaview_report.pdf", "rb") as file:
            btn = st.download_button(
                label="Download PDF",
                data=file,
                file_name="rheumaview_report.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please enter some findings before exporting.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 RheumaView™ | AI-assisted Radiologic Reasoning Platform")
