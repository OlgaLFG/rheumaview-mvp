import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="RheumaView MVP", layout="centered")

st.image("https://i.imgur.com/kGEkHRa.png", width=120)
st.title("🟩 RheumaView™")
st.subheader("Radiologic Reasoning for Rheumatologists")
st.caption("Curated by Dr. Olga Goodman")

st.image("https://upload.wikimedia.org/wikipedia/commons/2/26/Sacroiliac_joint_scheme.png", caption="Sacroiliac Joint Diagram", use_column_width=True)

st.markdown("---")

# Select mode
mode = st.radio("Choose interpretation mode:", ["Template Mode", "Manual Input (Smart Assist)"])

# Step 1: Select region
region = st.selectbox("Select anatomical region:", [
    "SI Joints",
    "Spine (DISH)",
    "Peripheral Joints – Hands",
    "Peripheral Joints – Feet"
])

# Step 2: Select confidence level
confidence = st.radio("Select confidence level:", ["Low", "Moderate", "High"])

# Optional manual input
description = ""
if mode == "Manual Input (Smart Assist)":
    description = st.text_area("Describe radiographic findings in your own words:",
                                placeholder="e.g., Mild sclerosis along iliac margins, symmetric appearance, no visible erosions...")
    st.markdown("**Suggested features to include:**")
    st.markdown("- Joint space narrowing\n- Erosions (marginal, central)\n- Sclerosis\n- Enthesophytes / osteophytes\n- Symmetry\n- Ankylosis / subluxation")

report = ""
# Step 3: Generate report
if st.button("Generate Report"):
    if mode == "Manual Input (Smart Assist)" and description:
        report = f"Interpretation based on user description for {region} (Confidence: {confidence}):\n\n" + description.strip()
    else:
        if region == "SI Joints":
            if confidence == "Low":
                report = ("Sacroiliac joints are symmetric. Mild subchondral sclerosis without erosions or joint space narrowing. "
                          "Findings may represent early sacroiliitis or degenerative change. Recommend MRI correlation if clinically warranted.")
            elif confidence == "Moderate":
                report = ("Mild irregularity and sclerosis of bilateral sacroiliac joints, more pronounced on iliac sides. "
                          "No erosions or ankylosis. Findings suggest early sacroiliitis.")
            else:
                report = ("Bilateral sacroiliac joint sclerosis, erosions, and joint space narrowing. "
                          "Findings consistent with Grade II–III sacroiliitis.")

        elif region == "Spine (DISH)":
            if confidence == "Moderate":
                report = ("Anterior vertebral body osteophytes and subtle ossification along the anterior longitudinal ligament at T12–L2, "
                          "with preserved disc spaces. Findings may be consistent with early DISH.")
            else:
                report = ("Flowing ossification along the anterior longitudinal ligament spanning T12 to L3 with preserved disc heights and "
                          "absence of significant degenerative change. Findings consistent with diffuse idiopathic skeletal hyperostosis (DISH).")

        elif region == "Peripheral Joints – Hands":
            if confidence == "Low":
                report = ("Mild joint space narrowing and subchondral sclerosis at bilateral DIP joints. No erosions. "
                          "Findings may reflect early degenerative changes.")
            elif confidence == "Moderate":
                report = ("Marginal erosions at the 2nd and 3rd MCP joints with symmetric joint space narrowing and juxta-articular osteopenia. "
                          "Findings suggest early inflammatory arthropathy (e.g., RA).")
            else:
                report = ("Symmetric marginal erosions with joint space narrowing at MCPs and MTPs, with juxta-articular osteopenia. "
                          "No osteophytes. Findings are consistent with erosive inflammatory arthritis, such as rheumatoid arthritis.")

        else:  # Peripheral Joints – Feet
            if confidence == "Low":
                report = ("Mild subchondral sclerosis and early osteophyte formation at 1st MTP joints. No erosions identified.")
            elif confidence == "Moderate":
                report = ("Joint space narrowing and juxta-articular osteopenia at multiple MTP joints with isolated marginal erosions. "
                          "Findings suggest evolving inflammatory arthropathy.")
            else:
                report = ("Prominent marginal erosions and joint space loss at multiple MTP joints with absence of osteophytes. "
                          "Findings consistent with advanced inflammatory arthritis.")

    st.markdown("### 📄 Generated Report:")
    st.success(report)

    # Export to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"RheumaView™ Report\n\nRegion: {region}\nConfidence: {confidence}\n\n{report}")
    pdf_file_path = "/tmp/rheumaview_report.pdf"
    pdf.output(pdf_file_path)

    with open(pdf_file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="RheumaView_Report.pdf">📥 Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)
