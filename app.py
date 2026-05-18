import streamlit as st
from core.pipeline import summarize_pipeline
import markdown as md

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
    background: radial-gradient(
        circle at top,
        #18243f 0%,
        #0B1020 35%,
        #050816 100%
    );
}

/* Title */

.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 800;
    letter-spacing: -1px;

    margin-bottom: 10px;

    background: linear-gradient(
        90deg,
        #4DA6FF,
        #A855F7
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */

.sub-text {
    text-align: center;
    font-size: 20px;
    color: #CFCFCF;

    margin-bottom: 38px;

    line-height: 1.7;
}

/* Buttons */

.stButton > button,
[data-testid="stFileUploader"] button {

    width: 100%;
    height: 52px;

    font-size: 16px;
    font-weight: 700;

    background: #1E293B !important;
    color: white !important;

    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;

    transition: all 0.25s ease !important;
}

.stButton > button:hover,
[data-testid="stFileUploader"] button:hover {

    background: #334155 !important;

    border: 1px solid rgba(255,255,255,0.16) !important;

    transform: translateY(-1px);

    box-shadow:
        0 0 16px rgba(77,166,255,0.06);
}

/* File uploader */

[data-testid="stFileUploader"] {

    border-radius: 22px;

    padding: 22px;

    margin-bottom: 24px;

    border: 1px solid rgba(255,255,255,0.08);

    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.04),
        rgba(255,255,255,0.018)
    );

    box-shadow:
        0 0 24px rgba(77,166,255,0.05);

    transition: all 0.25s ease;
}

[data-testid="stFileUploader"]:hover {

    border: 1px solid rgba(77,166,255,0.16);

    box-shadow:
        0 0 26px rgba(77,166,255,0.08);
}

/* Revision shell */

[data-testid="stVerticalBlockBorderWrapper"] {

    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.03),
        rgba(255,255,255,0.015)
    );

    border: 1px solid rgba(255,255,255,0.06);

    border-radius: 28px;

    padding: 26px;

    margin-top: 30px;

    box-shadow:
        0 0 28px rgba(77,166,255,0.05);
}

/* Expanders */

.stExpander {
    margin-bottom: 18px;
}

[data-testid="stExpander"] {

    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.035),
        rgba(255,255,255,0.015)
    );

    border: 1px solid rgba(255,255,255,0.05);

    border-radius: 18px;

    overflow: hidden;

    backdrop-filter: blur(8px);

    transition: all 0.25s ease;
}

[data-testid="stExpander"]:hover {

    border: 1px solid rgba(77,166,255,0.10);

    box-shadow:
        0 0 18px rgba(77,166,255,0.05);
}

/* Expander header */

[data-testid="stExpander"] summary {

    padding-top: 6px;
    padding-bottom: 6px;

    font-size: 17px;
    font-weight: 600;

    color: #E5E7EB;
}

/* Expander content */

[data-testid="stExpanderDetails"] {

    padding-top: 8px;
    padding-bottom: 8px;
}

[data-testid="stExpanderDetails"] p,
[data-testid="stExpanderDetails"] li {

    color: #D6D9E0;

    font-size: 16px;

    line-height: 1.85;
}

/* Question headings */

[data-testid="stExpanderDetails"] h3 {

    margin-top: 22px;
    margin-bottom: 10px;

    font-size: 24px;

    color: #F3F4F6;
}

/* Answer blocks */

blockquote {

    border-left: 2px solid rgba(77,166,255,0.22);

    padding-left: 14px;

    color: #B8C0CC;

    margin-top: 10px;
    margin-bottom: 18px;
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
    max_upload_size=50,
)

st.caption("Recommended: Clear English PDFs under 75 pages for best results.")


if uploaded_file is not None:
    if st.button("Summarize"):
        with st.spinner("Summarizing...."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            data = summarize_pipeline("temp.pdf")
            if data:

                with st.container(border=True):

                    # High priority revision
                    revision_content = "\n".join(
                        f"- {point}"
                        for point in data.get("high_priority_revision", [])
                    )

                    with st.expander("🔥 High Priority Revision", expanded=True):
                        st.markdown(revision_content)

                    # Important QnA
                    qna_content = "\n\n".join(
                        f"### Q. {item['question']}\n\n> {item['answer']}"
                        for item in data.get("exam_questions", [])
                    )

                    with st.expander("❓ Important QnA"):
                        st.markdown(qna_content)

                    # Keywords
                    keyword_content = "\n\n".join(
                        f"### {item['term']}\n\n> {item['definition']}"
                        for item in data.get("keywords", [])
                    )

                    with st.expander("📘 Important Keywords"):
                        st.markdown(keyword_content)

                st.success("Notes generated successfully!")



