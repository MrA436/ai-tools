import streamlit as st
from core.pipeline import generate_notes, extract_text_from_pdf

st.set_page_config(page_title="Revizen", layout="centered")
st.markdown("""

<style>

/* Layout */
.block-container {
    padding-top: 3rem;
    max-width: 900px;
}

/* Background */
.stApp {
    background: radial-gradient(circle at top,
    #18243f 0%,
    #0B1020 35%,
    #050816 100%);
}

/* Title */
.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -1px;

    background: linear-gradient(90deg, #4DA6FF, #A855F7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.sub-text {
    text-align: center;
    font-size: 20px;
    color: #CFCFCF;
    margin-bottom: 35px;
    line-height: 1.7;
}

/* Shared button styles */
.stButton > button,
.stDownloadButton > button,
[data-testid="stFileUploader"] button {

    background: #1E293B !important;
    color: white !important;

    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;

    transition: all 0.2s ease !important;
}

/* Main button sizing */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    height: 52px;
    font-size: 16px;
    font-weight: 700;
}

/* Shared hover */
.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stFileUploader"] button:hover {

    background: #334155 !important;
    border: 1px solid rgba(255,255,255,0.18) !important;

    transform: translateY(-1px);
}

/* File uploader */
[data-testid="stFileUploader"] {

    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;

    padding: 14px;

    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.04),
        rgba(255,255,255,0.02)
    );

    box-shadow:
        0 0 20px rgba(77,166,255,0.05);

    transition: all 0.25s ease;
}

/* Upload box hover */
[data-testid="stFileUploader"]:hover {

    border: 1px solid rgba(77,166,255,0.25);

    box-shadow:
        0 0 28px rgba(77,166,255,0.12);

    transform: translateY(-1px);
}

/* Text area */
textarea {
    border-radius: 14px !important;
    background-color: rgba(255,255,255,0.03) !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

</style>

""", unsafe_allow_html=True)

st.markdown("""

<div class="main-title">
Revizen
</div>

<div class="sub-text">
Turn boring PDFs into clean summaries, exam questions,
revision notes, and rapid study material instantly.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Study Material",
    type="pdf",
    max_upload_size=50
)

st.caption(
    "Recommended: Clear English PDFs under 75 pages for best results."
)

if uploaded_file is not None:
    if st.button("Summarize"):
        with st.spinner("Summarizing...."):
            with open("temp.pdf","wb") as f:
                f.write(uploaded_file.getbuffer())
            text = extract_text_from_pdf("temp.pdf")
            notes = generate_notes(text)  
            st.text_area(label = "Genrated Notes",value = notes, height = 500)
            st.download_button(label = "Download Notes", data = notes, file_name="output.txt")
            st.success("Notes generated successfully!")

