# RheumaView™ — System Requirements and Feature Specification

---

### 🔐 Access and Usage
- Only licensed clinicians or authorized medical professionals may use the app.
- Monthly user confirmation required to continue using the app (via checkbox or simplified signature).
- Electronic signature supported.
- Registration data editable at any time.
- The system performs periodic checks to verify eligibility to use the app.

### 📷 Image Upload and Region Recognition
1. **Multiple File Uploads**
   - Upload images in any order.
   - System automatically sorts and groups by anatomical region.
   - Max image count and resolution only limited by platform capacity.

2. **Formats Supported**
   - JPG, PNG, WEBP, BMP, TIFF, DICOM (.dcm)

3. **View Count Recognition**
   - System counts number of views per region.
   - Confirmation optional.

4. **Instant Preview & Region Guess**
   - Region classification shown per image.
   - Optional manual override (not required).

### 🗓️ Study Date Handling
- Default to today's date.
- Calendar override allowed (Y/M/D or partial).

### 🔹 Report Type Selection
- **Single Report**
- **Report with Comparison** to 1+ prior blocks

### 🌐 Anatomical Region Selection
- Default: *Multiple Regions*
- Dropdown: cervical spine, thoracic spine, lumbar spine, pelvis/SI/sacrum, hips, knees, ankles, feet, hands, wrists, elbows, shoulders, others
- If *Multiple Regions* selected, system groups and reports by region:
  > e.g., "Thoracic spine – 2 views, Lumbar spine – 5 views, Right hand – 3 views, Left hand – 3 views"

### ✏️ Demographic Inputs
- Age or Date of Birth (auto-calculate age)
- Sex at birth
- Optional: Name/Initials, MRN, custom header/footer
- Header and footer are retained across sessions unless changed by user

### ⚠️ Disclaimer and Curation Statement
- Always displayed in app and included in reports:
  > “This app does not perform automated radiologic interpretation or image recognition. All reports are user-generated and edited. No PHI is stored. Curated by Dr. Olga Goodman.”
- Logo included in interface.
- All entered data is either deleted upon user confirmation or automatically after 30 minutes of inactivity post-report generation.
- If the user opts to retain a file for further editing, it is stored temporarily **without patient name** in a secure folder for: 24, 48, 72 hours, or 7 days — user-selectable.
- Users confirm full responsibility for HIPAA compliance.

---

### 🔢 Interpretation Protocol
- **READY** flag required to begin interpretation.
- Clinical context is allowed for internal logic but never included in reports.
- Number and type of views per region are stated.
- Use bold anatomical headers.
- Spine and SI joints assessed per inflammatory/degenerative standards.

---

### 📊 Prior Imaging Comparison Logic
- Only current-uploaded regions are reported.
- Prior images are compared **only if matching anatomical region exists**.
- If additional regions exist in prior sets:
  - System prompts user: *"Include addendum for unmatched regions?"*
  - If yes: Addendum added with date and disclaimer that findings based solely on prior study.

---

### 📄 Report Format
- Generated in `.docx`, editable
- **EMR Summary** auto-displayed after READY:
  - Single report: ≤ 700 characters
  - With comparison: ≤ 1000 characters
  - No demographics, structured for pasting into EMR

---

### 🧠 AI Functionality
- **Confidence Slider**: toggle for High Confidence vs. Probable Findings
- **Diagnostic Pattern Tag**: shows summary label (e.g., "Suggests RA", "No inflammatory changes")

---

### 📋 Export Features
- **PDF Export** after user review
  - Warning shown: *"The system is not responsible for user edits. Proceed?"*
  - Final PDF includes:
    - Header/footer, disclaimer
    - Statement: *"This report has been reviewed and modified as necessary by [user name], who accepts responsibility for all interpretations and changes herein."*
    - Optional electronic signature

---

### 🔄 Report Shortening Tool
- Optional: generate **Concise Report**
  - Compression options: 75%, 50%, or char limits (10k / 7.5k / 5k)
  - If loss of detail would be significant, system warns and requires confirmation

---

### 🖊️ Peripheral Joint Radiograph Protocol
- **Joint Space Narrowing**: symmetry, severity, and joint distribution (e.g., MCPs, PIPs)
- **Erosions**: location (marginal, central), count, morphology (e.g., sharply marginated, overhanging)
- **Bone Density**: presence of juxta-articular osteopenia or subchondral sclerosis
- **Osteophytes / Bone Proliferation**: typical vs atypical for OA
- **Soft Tissue Changes**: swelling, effusion, tophi, tenosynovitis
- **Calcifications**: punctate, chondrocalcinosis (CPPD)
- **Enthesopathy**: enthesophytes or active enthesitis
- **Alignment/Deformity**: subluxation, deviation, ankylosis
- All assessments follow disease-specific patterns (RA, PsA, gout, EOA, OA)
- Addendum templates follow structured summary language with low/moderate/high confidence variants