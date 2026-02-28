import os
import shutil
from pathlib import Path

# Try to import required libraries and provide clear error messages if missing
try:
    from PIL import Image
    import torch
    from transformers import pipeline
    from tqdm import tqdm
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Please install the required libraries by running:")
    print("pip3 install torch torchvision transformers pillow pillow-heif tqdm")
    exit(1)

# Register HEIF opener for Apple's HEIC image format
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("Warning: pillow-heif is not installed. HEIC images (default on iPhone) will be skipped.")
    print("To support them, run: pip3 install pillow-heif")

# Configuration
SOURCE_DIR = "/memories"
DEST_DIR = "/memories/best"
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.heic'}

# We use the CLIP model which is excellent at understanding both image content and quality from text
MODEL_NAME = "openai/clip-vit-base-patch32"

# Prompts for classification. We want appealing photos of people or nature, 
# and we want to penalize bad, blurry, or random irrelevant photos.
CANDIDATE_LABELS = [
    "A stunning, high quality, beautiful portrait or photograph of people",
    "A stunning, high quality, beautiful photograph of nature or landscapes",
    "A low quality, blurry, dark, or unattractive photo",
    "A screenshot, document, text, or random object"
]

# We will consider a photo "Best" if the combined probability of the first two labels exceeds this threshold.
# Adjust this threshold if you're getting too many or too few photos. 
# 0.70 means the model is 70% confident it's a beautiful photo of people/nature vs the negative labels.
THRESHOLD = 0.70

def is_image(filepath):
    return Path(filepath).suffix.lower() in SUPPORTED_EXTENSIONS

def filter_photos():
    print("Setting up the AI model (this may take a moment to download the first time)...")
    # Use GPU if available (Metal Performance Shaders on Mac)
    device = 0 if torch.backends.mps.is_available() else -1
    if device == 0:
         print("Using Apple Silicon GPU for faster processing!")
    
    classifier = pipeline("zero-shot-image-classification", model=MODEL_NAME, device=device)
    
    # Ensure destination folder exists
    os.makedirs(DEST_DIR, exist_ok=True)
    
    # Gather all image files
    all_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        if DEST_DIR in root:
            continue # Skip the destination folder
        for file in files:
            if is_image(file):
                all_files.append(os.path.join(root, file))
                
    print(f"Found {len(all_files)} images to analyze in the Memories folder.")
    if len(all_files) == 0:
        print("No images found.")
        return

    # Process images
    selected_count = 0
    error_count = 0
    
    for filepath in tqdm(all_files, desc="Analyzing Photos"):
        try:
            # Open the image
            with Image.open(filepath) as img:
                # Convert to RGB if needed (e.g., RGBA or single channel)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Classify the image
                results = classifier(img, candidate_labels=CANDIDATE_LABELS)
                
                # The pipeline returns a list of dictionaries with 'score' and 'label'
                # We sum the scores of the "good" labels
                good_score = 0.0
                for result in results:
                    if "quality, beautiful" in result["label"]:
                        good_score += result["score"]
                
                # If the score passes our threshold, we copy the file
                if good_score >= THRESHOLD:
                    filename = os.path.basename(filepath)
                    dest_path = os.path.join(DEST_DIR, filename)
                    
                    # Handle duplicate filenames by appending a number if necessary
                    base_name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(DEST_DIR, f"{base_name}_{counter}{ext}")
                        counter += 1
                        
                    shutil.copy2(filepath, dest_path)
                    selected_count += 1
                    
        except Exception as e:
            error_count += 1
            # print(f"\nCould not process {filepath}: {e}")
            continue

    print("-" * 40)
    print("Analysis Complete!")
    print(f"Selected and copied {selected_count} photos to {DEST_DIR}")
    if error_count > 0:
        print(f"Skipped {error_count} unreadable or corrupt files.")

if __name__ == "__main__":
    filter_photos()
