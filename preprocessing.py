import cv2               # OpenCV for image processing
import os                # To handle file paths and folders

# Folders where the original OMR images are stored
data_folders = [
    r"C:\Users\Areeba\Desktop\omr-evaluation-system\data\Set A",
    r"C:\Users\Areeba\Desktop\omr-evaluation-system\data\Set B"
]

# Folder where preprocessed images will be saved
outputs_folder = r"C:\Users\Areeba\Desktop\omr-evaluation-system\outputs"

# Create output folder if it does not exist
if not os.path.exists(outputs_folder):
    os.makedirs(outputs_folder)

# Loop through each folder and each image inside
for folder in data_folders:
    for filename in os.listdir(folder):
        # Process only image files
        if filename.endswith((".jpg", ".jpeg", ".png")):
            # Full path to the current image
            image_path = os.path.join(folder, filename)
            
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to read image: {image_path}")
                continue  # Skip to next image if reading fails

            # Convert to grayscale (simpler for bubble detection)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur to reduce noise and small shadows
            blurred = cv2.GaussianBlur(gray, (5,5), 0)

            # Apply binary thresholding to highlight filled bubbles
            _, thresh = cv2.threshold(
                blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )

            # Save the processed image to outputs folder
            output_path = os.path.join(outputs_folder, filename)
            cv2.imwrite(output_path, thresh)

            print(f"Preprocessed image saved: {output_path}")
