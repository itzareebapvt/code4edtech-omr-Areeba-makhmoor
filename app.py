import streamlit as st
import cv2
import numpy as np
from utils import detect_answers_from_image  # your function

st.set_page_config(page_title="OMR Sheet Evaluator", layout="wide")
st.title("📄 OMR Sheet Evaluator")

# ----------------------------
# File Uploader
# ----------------------------
uploaded_files = st.file_uploader(
    "Upload one or more OMR sheets", type=["png", "jpg", "jpeg"], accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

    results = []

    for uploaded_file in uploaded_files:
        # Convert uploaded file to OpenCV image
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            st.error(f"❌ Error reading {uploaded_file.name}. Please upload a valid image.")
            continue

        st.image(image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)

        # Detect answers (replace with your actual bubble detection logic)
        try:
            detected_answers = detect_answers_from_image(image)
        except Exception as e:
            st.error(f"Error detecting answers in {uploaded_file.name}: {e}")
            detected_answers = {}

        st.write(f"✅ Detected Answers for {uploaded_file.name}:")
        st.json(detected_answers)

        results.append({"file": uploaded_file.name, "answers": detected_answers})

    # Optional: Show summary table
    if results:
        st.subheader("Summary of Detected Answers")
        for r in results:
            st.write(f"**{r['file']}**: {r['answers']}")

else:
    st.info("Please upload at least one OMR sheet to get started.")
