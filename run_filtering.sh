#!/bin/bash
echo "Installing required Python libraries for AI Photo Filtering..."
pip3 install torch torchvision transformers pillow pillow-heif tqdm

echo ""
echo "Starting the filtering process..."
python3 filter_best_photos.py
