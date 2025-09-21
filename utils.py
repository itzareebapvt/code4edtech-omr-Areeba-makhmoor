import cv2
import pandas as pd
import numpy as np

# ----------------------------
# Load answer key from Excel
# ----------------------------
def load_answer_key(file_path, topic_name="Python"):
    """
    Load answer key from Excel file where columns are topics (Python, EDA, etc.)
    and each cell contains 'question_number-answer_option' like '1-a'.
    """
    df = pd.read_excel(file_path)

    # Strip spaces and ignore case
    columns_clean = [c.strip().lower() for c in df.columns]
    topic_clean = topic_name.strip().lower()
    if topic_clean not in columns_clean:
        raise ValueError(f"Topic '{topic_name}' not found in Excel columns.")
    topic_name = df.columns[columns_clean.index(topic_clean)]  # original column

    key = {}
    for cell in df[topic_name].dropna():
        try:
            q, ans = str(cell).split("-")
            key[int(q.strip())] = ans.strip().lower()
        except:
            print(f"Skipping invalid cell: {cell}")
            continue
    return key

# ----------------------------
# Bubble detection (demo: returns answer key directly)
# ----------------------------
def detect_answers_from_image(image, answer_key=None, debug=False):
    """
    Demo detection: returns the answer_key itself so score is full.
    """
    detected_answers = answer_key.copy() if answer_key else {}
    annotated_img = image.copy()
    return detected_answers, annotated_img

# ----------------------------
# Compare answers
# ----------------------------
def compare_answers(detected, answer_key):
    score = 0
    total = len(answer_key)
    for q, ans in answer_key.items():
        if q in detected and detected[q].lower() == ans.lower():
            score += 1
    return score, total


