import cv2

# Load the image
img = cv2.imread('MidTerm/filtered_data/page_057.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply threshold to separate text from background
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize a list to store the bounding boxes
bboxes = []

# Iterate through the contours and create bounding boxes
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Filter out small contours (likely not text)
    if h > 20 and w > 20:
        bboxes.append((x, y, x+w, y+h))

# Print the bounding box coordinates
for bbox in bboxes:
    x1, y1, x2, y2 = bbox
    print(f"Dòng văn bản: ({x1}, {y1}, {x2}, {y2})")