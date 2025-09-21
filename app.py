import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import detect_answers_from_image, load_answer_key, compare_answers

st.set_page_config(page_title="OMR Evaluation", layout="wide")

# ---------------------------- Page Background & CSS ----------------------------
st.markdown("""
<style>
/* Full page background */
[data-testid="stAppViewContainer"] {
    background-color: #a5d6a7;  /* light green */
    color: #1b5e20;
}

/* Title */
h1 {
    color: #1b5e20;  
    text-align: center;
    font-weight: bold;
}

/* Input cards */
.key-topic-container {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    justify-content: center;
}
.key-topic-container > div {
    background-color: #c8e6c9;  /* lighter card green */
    padding: 25px;
    border-radius: 15px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.2);
    flex: 1;
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    color: #1b5e20;
}

/* Drag and drop */
.stFileUploader>div {
    border: 3px dashed #2e7d32;
    border-radius: 20px;
    background-color: #e8f5e9;
    padding: 60px;
    text-align: center;
    font-size: 18px;
    color: #1b5e20;
    margin: auto;
    margin-bottom: 20px;
    transition: 0.3s;
    width: 80%;
}
.stFileUploader>div:hover {
    border-color: #1b5e20;
    background-color: #c8e6c9;
}

/* Change Browse File button color */
.stFileUploader button {
    background-color: #66bb6a !important;  /* light green */
    color: white !important;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: bold;
    border: none;
}
.stFileUploader button:hover {
    background-color: #43a047 !important; 
}

/* Score boxes */
.score-box {
    background-color: #66bb6a;
    color: white;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    font-weight: bold;
}

/* Summary box */
.summary-box {
    background-color: #2e7d32;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
    color: white;
}

/* OMR image styling */
.omr-image {
    border: 3px solid #2e7d32;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------- Title ----------------------------
st.title("📝 OMR Sheet Evaluation System")

# ---------------------------- Key and Topic Inputs ----------------------------
col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('<div class="key-topic-container"><div>📄 Upload Answer Key Excel</div></div>', unsafe_allow_html=True)
    answer_key_file = st.file_uploader("", type=["xlsx"], key="key_file")
with col2:
    st.markdown('<div class="key-topic-container"><div>🖊️ Enter Topic Name</div></div>', unsafe_allow_html=True)
    topic_name = st.text_input("", "Python", key="topic_name")

# ---------------------------- Drag & Drop OMR Upload ----------------------------
uploaded_files = st.file_uploader(
    "📂 Upload OMR Sheet Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ---------------------------- Evaluation ----------------------------
if answer_key_file and uploaded_files:
    try:
        answer_key = load_answer_key(answer_key_file, topic_name)
        st.success(f"✅ Loaded answer key for topic '{topic_name}'")
    except Exception as e:
        st.error(f"Error loading answer key: {e}")
        st.stop()

    st.header("📊 OMR Evaluation Results")
    summary_scores = {}

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        try:
            detected_answers, annotated_img = detect_answers_from_image(image_cv, answer_key)
        except Exception as e:
            st.error(f"Error detecting answers for {uploaded_file.name}: {e}")
            continue

        score, total = compare_answers(detected_answers, answer_key)
        summary_scores[uploaded_file.name] = f"{score} / {total}"

        # Score box
        st.markdown(f'<div class="score-box">{uploaded_file.name} → Score: {score}/{total}</div>', unsafe_allow_html=True)

        # Detected answers
        st.subheader("✅ Detected Answers:")
        st.json(detected_answers)

        # Display annotated OMR image (resized)
        annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        st.image(annotated_img_rgb, caption="Detected Bubbles Overlay", use_column_width=True, output_format="PNG", clamp=True)

    # Summary box
    st.header("📋 Summary of All Sheets")
    summary_html = "<div class='summary-box'>"
    for fname, scr in summary_scores.items():
        summary_html += f"<p><b>{fname}:</b> {scr}</p>"
    summary_html += "</div>"
    st.markdown(summary_html, unsafe_allow_html=True)

else:
    st.info("Upload the answer key and at least one OMR sheet image to start evaluation.")
