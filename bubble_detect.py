# bubble_detect.py

import os
import cv2
from utils import read_image, threshold_image, find_contours, get_bubble_boxes, extract_answers

input_folder = r"C:\Users\Areeba\Desktop\omr-evaluation-system\omr\raw_sheets"
output_folder = r"C:\Users\Areeba\Desktop\omr-evaluation-system\omr\bubble_outputs"
set_name = "Set - A"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(input_folder, filename)

        gray, original_image = read_image(image_path)
        thresh = threshold_image(gray)
        contours = find_contours(thresh)
        bubble_boxes = get_bubble_boxes(contours)
        detected_answers_list = extract_answers(thresh, bubble_boxes, set_name)

        # Optional: save image with detected bubbles highlighted
        for i, box in enumerate(bubble_boxes):
            x, y, w, h = box
            color = (0, 255, 0) if detected_answers_list[i] else (0, 0, 255)
            cv2.rectangle(original_image, (x, y), (x+w, y+h), color, 2)

        save_path = os.path.join(output_folder, filename)
        cv2.imwrite(save_path, original_image)
        print(f"Processed: {filename}")
