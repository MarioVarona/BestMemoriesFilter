import os
import hashlib
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm
from send2trash import send2trash

# Configuration
TARGET_DIR = "/memories/best"

def get_file_hash(filepath, block_size=65536):
    """Generates an MD5 hash of the file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(block_size)
    return hasher.hexdigest()

def remove_duplicates():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory {TARGET_DIR} does not exist.")
        return

    print(f"Scanning directory: {TARGET_DIR}")
    
    # Gather all files in the directory
    all_files = []
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            # Skip hidden files like .DS_Store
            if file.startswith('.'):
                continue
            all_files.append(os.path.join(root, file))

    if not all_files:
        print("No files found.")
        return

    print(f"Found {len(all_files)} files to check for duplicates.")

    # Dictionary to map hash to a list of file paths
    hash_to_files = defaultdict(list)
    
    # Calculate hashes for all files
    for filepath in tqdm(all_files, desc="Calculating Hashes"):
        try:
            file_hash = get_file_hash(filepath)
            hash_to_files[file_hash].append(filepath)
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")

    # Identify and remove duplicates
    duplicates_removed = 0
    bytes_freed = 0

    print("\nRemoving duplicates...")
    for file_hash, filepaths in hash_to_files.items():
        if len(filepaths) > 1:
            # Keep the first file, remove the rest
            original_file = filepaths[0]
            duplicates = filepaths[1:]
            
            for duplicate in duplicates:
                try:
                    file_size = os.path.getsize(duplicate)
                    send2trash(duplicate)
                    duplicates_removed += 1
                    bytes_freed += file_size
                    # print(f"Removed: {duplicate}") # Uncomment to see what's being removed
                except Exception as e:
                    print(f"Error removing file {duplicate}: {e}")

    print("-" * 40)
    print("Duplicate Removal Complete!")
    print(f"Total duplicate files removed: {duplicates_removed}")
    print(f"Space freed: {bytes_freed / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    remove_duplicates()
