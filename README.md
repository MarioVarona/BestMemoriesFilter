# Best Memories Filter

This repository contains a collection of scripts designed to help curate and manage your photo collection, specifically tailored for selecting the best memories for digital frames or personal archives.

## Scripts Overview

- **`run_filtering.sh`**: The main entry point. It installs necessary dependencies and starts the AI-powered filtering process.
- **`filter_best_photos.py`**: An AI-powered tool that uses the OpenAI CLIP (Contrastive Language-Image Pre-training) model to analyze photos. It selects high-quality images of people and nature while filtering out blurry, dark, or irrelevant photos (like screenshots).
- **`remove_duplicates.py`**: A utility to scan the `Best/` folder and remove duplicate images using MD5 hashing to ensure a unique collection.
- **`heic_to_jpg.sh`**: A bash script that uses macOS's `sips` tool to convert Apple's HEIC format images to standard JPG files.

## How to Use

1. **Export Photos**: Open the macOS Photos app (or any other Photos app).
2. **From Memories**: Navigate to the **Memories** feature.
3. **Export**: Select the memory you want to use, and export the photos to a local folder.
4. **Prepare for Filtering**: Place the exported images into the root of this repository.
5. **Run Script**: Execute `./run_filtering.sh` to begin the AI curation.

## Folders

The scripts are designed to process images directly within the current directory.

- **`Best/`**: The default destination folder where the "best" filtered photos are copied.

## Requirements

The Python scripts require several libraries including `torch`, `transformers`, `pillow`, and `tqdm`. These can be installed via the `run_filtering.sh` script or manually using `pip`.
