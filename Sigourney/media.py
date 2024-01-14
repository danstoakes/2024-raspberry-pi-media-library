try:
    from flask import url_for
    import json
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

def get_films(directory, page=1, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page

    all_films = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    films = all_films[start:end]

    return films

from flask import url_for
import os
import json

def get_tv_shows(directory, thumbnails_directory, page=1, per_page=32):
    shows = next(os.walk(directory))[1]
    shows_metadata = []

    shows = [show for show in shows if show != "category-thumbnails"]

    shows.sort()

    start = (page - 1) * per_page
    end = start + per_page
    paginated_shows = shows[start:end]

    for show_folder in paginated_shows:
        metadata_path = os.path.join(directory, show_folder, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                thumbnail_file = os.path.splitext(show_folder)[0] + ".png"
                thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
                thumbnail_url = url_for("static", filename=thumbnail_relative_path)

                shows_metadata.append({
                    "title": metadata.get("title"),
                    "thumbnail": thumbnail_url,
                    "slug": f"/tv-shows/{show_folder}"
                })

    return shows_metadata

def get_videos(directory, thumbnails_directory, page=1, per_page=32):
    start = (page - 1) * per_page
    end = start + per_page

    all_videos = [f for f in os.listdir(os.path.join('static', directory)) if os.path.isfile(os.path.join('static', directory, f))]
    videos = all_videos[start:end]

    video_thumbnail_pairs = []

    for video in videos:
        thumbnail_file = os.path.splitext(video)[0] + ".png"
        thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)

        if os.path.isfile(os.path.join("static", thumbnail_relative_path)):
            thumbnail = thumbnail_relative_path
        else:
            thumbnail = "/thumbnails/fallback.png"

        video_thumbnail_pairs.append({
            "video": os.path.join(directory, video),
            "thumbnail": thumbnail
        })

    return video_thumbnail_pairs