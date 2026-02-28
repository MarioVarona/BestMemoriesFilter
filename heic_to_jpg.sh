#!/bin/bash

shopt -s nullglob nocaseglob

files=( *.heic )

for f in "${files[@]}"; do
  if sips -s format jpeg "$f" --out "${f%.*}.jpg"; then
    rm "$f"
  else
    echo "Failed to convert $f"
  fi
done