-OMR Sheet Evaluation System
-
**About the Project**

This project is an OMR (Optical Mark Recognition) Sheet Evaluation System that allows you to automatically evaluate multiple-choice answer sheets. The system can process scanned OMR sheets, detect marked answers, and calculate scores based on a provided answer key. The results include per-question correctness and overall scores, presented in a user-friendly interface.

The project also includes a web application built using Streamlit to make the evaluation interactive and visually appealing.

-Features
-
-Upload multiple OMR sheet images at once.

-Upload the answer key in Excel format (supports multiple subjects).

-Automatically evaluate answers using a pre-defined detection logic.

-Display the detected answers and scores in an organized and aesthetic interface.

-Interactive and engaging UI with drag-and-drop file upload, colored result cards, and annotated OMR sheets.

-How It Works
-
-Preprocessing

Original OMR sheets are processed to highlight marked bubbles (red and green overlay). This step ensures that the detection works reliably.

-Bubble Detection

The system detects the filled bubbles on the processed OMR sheets. The detection is visualized with colored boxes: green indicates a detected answer, red indicates unmarked or skipped bubbles.

-Evaluation

The system compares the detected answers with the provided answer key. The evaluation returns:

-Total score

Per-question correctness

-Annotated images showing detected bubbles

-Streamlit App
 The app allows users to upload OMR sheets and answer keys directly in the browser. Results are displayed with clear score cards and images with highlighted answers.

-Repo Structure
-
**The repository includes the following files:**

**Key (Excel file)** – Contains the answer key for different subjects (Python, EDA, SQL, etc.). This is required by the app to evaluate OMR sheets.

**app.py**– The main Streamlit application that runs the OMR evaluation interface. This is the core file users will interact with.

**evaluator.py**– Contains the logic to compare detected answers with the answer key and calculate the score.

**utils.py**– Helper functions for loading the answer key, detecting answers (demo), and comparing them.

**Image**– Sample OMR sheet image used for testing or demo purposes

-How to Use
-
**Clone the repository:**

git clone <>
cd omr-evaluation-system


**Install dependencies:**

pip install streamlit opencv-python pandas numpy pillow


**Run the app:**

streamlit run app.py


**In the app interface:**

-Upload the Excel answer key file.

-Enter the subject name (e.g., Python, EDA).

-Upload OMR sheet images (multiple files supported).

-View the detected answers, annotated OMR images, and total scores.

**Notes**

The app currently uses a demo detection logic for generating detected answers, which is sufficient for presentation and demonstration purposes.

The Streamlit interface has been customized for aesthetics with drag-and-drop file upload, colored cards, and organized score display.

-Future Work
-
Integrate real bubble detection to generate accurate answers from raw OMR sheets.

Support more complex answer sheet formats with multiple columns and subjects.

Enhance UI further with responsive design and additional analytics.
