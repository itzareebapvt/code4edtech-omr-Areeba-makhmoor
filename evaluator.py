# evaluator.py

import os
import pandas as pd
from utils import detect_answers_from_image, compare_answers

# ----------------------------
# SETTINGS
# ----------------------------
set_name = "Set - A"
bubble_output_folder = r"C:\Users\Areeba\Desktop\omr-evaluation-system\omr\bubble_outputs"
excel_file = r"C:\Users\Areeba\Desktop\omr-evaluation-system\data\Keys\Key (Set A and B).xlsx"

# ----------------------------
# LOAD ANSWER KEY
# ----------------------------
print(f"Loading answer key for {set_name}...")

# Read Excel
df = pd.read_excel(excel_file)

# Standardize column names: remove spaces and lowercase
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

# Build answer key dict
answer_key = {}
for _, row in df.iterrows():
    qnum = int(row["questionnumber"])  # Excel column for question numbers
    if set_name.lower() == "set - a":
        answer_key[qnum] = row["optionset_a"]  # standardized column
    else:
        answer_key[qnum] = row["optionset_b"]

print("✅ Answer key loaded successfully!\n")

# ----------------------------
# EVALUATE EACH SHEET
# ----------------------------
print("Evaluating OMR sheets...\n")

for filename in os.listdir(bubble_output_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(bubble_output_folder, filename)

        try:
            # Detect answers
            detected_answers = detect_answers_from_image(image_path, set_name=set_name)
        except Exception as e:
            print(f"❌ Error detecting answers for {filename}: {e}")
            continue

        # Compare with answer key
        score, total = compare_answers(detected_answers, answer_key)

        # Print results
        print(f"File: {filename}")
        print(f"Detected answers: {detected_answers}")
        print(f"Score: {score} / {total}\n")

print("✅ Evaluation completed for all sheets!")
