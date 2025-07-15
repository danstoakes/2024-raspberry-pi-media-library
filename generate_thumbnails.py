import Sigourney as sigourney
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
THUMBNAILS_BASE = os.path.join(STATIC_DIR, "thumbnails")

EXCLUDED_DIRS = {"js", "css", "films"}

def generate_thumbnails_with_structure(media_root, thumbnails_root):
    for root, _, files in os.walk(media_root):
        for file in files:
            if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                
                # Relative path from the media root
                relative_path = os.path.relpath(video_path, start=media_root)
                
                # Destination thumbnail path with matching structure and .jpg extension
                thumbnail_rel_path = os.path.splitext(relative_path)[0] + ".jpg"
                thumbnail_path = os.path.join(thumbnails_root, thumbnail_rel_path)

                # Ensure parent dirs exist
                os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

                # Generate thumbnail
                sigourney.media.generate_video_thumbnail(video_path, thumbnail_path)

# Loop through top-level static folders (excluding js/css)
for entry in os.listdir(STATIC_DIR):
    entry_path = os.path.join(STATIC_DIR, entry)
    if os.path.isdir(entry_path) and entry not in EXCLUDED_DIRS:
        media_directory = entry_path
        thumbnails_directory = os.path.join(THUMBNAILS_BASE, entry)

        print(f"Generating thumbnails for: {media_directory}")
        generate_thumbnails_with_structure(media_directory, thumbnails_directory)