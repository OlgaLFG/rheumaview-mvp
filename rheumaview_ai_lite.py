
import streamlit as st
import datetime
from docx import Document

st.set_page_config(page_title="RheumaView AI Lite — TEST MODE", layout="wide")

st.title("RheumaView AI Lite — TEST MODE")
st.caption("This is a diagnostic version. Output should contain one hardcoded phrase.")

study_date = st.date_input("Date of current study", datetime.date.today())
age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
sex = st.radio("Sex at Birth", ["Female", "Male", "Other / Intersex"])
name = st.text_input("Patient Name", value="Test Name")
mrn = st.text_input("Medical Record Number", value="0000000")
dob_input = st.text_input("Date of Birth (YYYY-MM-DD)", value="1990-01-01")

st.markdown("---")

if st.button("Generate Test Report"):
    doc = Document()
    doc.add_paragraph("TEST HEADER")
    doc.add_heading("RheumaView Structured Report", 0)
    doc.add_paragraph(f"Date of Current Study: {study_date}")
    doc.add_paragraph(f"Patient: {name}")
    doc.add_paragraph(f"DOB: {dob_input}")
    doc.add_paragraph(f"MRN: {mrn}")
    doc.add_paragraph(f"Age: {age}")
    doc.add_paragraph(f"Sex: {sex}")
    doc.add_heading("RheumaView Report", level=1)
    doc.add_paragraph("THIS IS A TEST REPORT BODY")
    doc.add_heading("Interval Comparison", level=2)
    doc.add_paragraph("Prior_1 (): Compared for progression/regression relative to current study.")
    doc.add_paragraph("TEST FOOTER")

    filename = "rheumaview_structured_report_TEST_OUTPUT.docx"
    doc.save(filename)

    with open(filename, "rb") as file:
        st.download_button("⬇️ Download TEST Report", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    st.success("✅ Test report generated. Check for presence of fixed phrase.")
