import os
import cv2
import torch
import easyocr
import glob

# Load YOLOv5 model (requires best.pt to be in the root folder)
model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')

# Path to test image
image_path = 'images/car.jpg'

# Run detection
results = model(image_path)
results.save()  # Saves image + crops in runs/detect/exp/

# Locate the latest output directory (exp, exp2, ...)
output_dir = sorted(glob.glob('runs/detect/exp*'), key=os.path.getmtime)[-1]
crop_dir = os.path.join(output_dir, 'crops')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Run OCR on each cropped license plate image
for root, _, files in os.walk(crop_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.png')):
            plate_path = os.path.join(root, file)
            print(f"\n🔍 OCR on: {file}")
            ocr_result = reader.readtext(plate_path)
            if ocr_result:
                for det in ocr_result:
                    print("🪪 Detected Plate Number:", det[1])
            else:
                print("⚠️ No text detected")

