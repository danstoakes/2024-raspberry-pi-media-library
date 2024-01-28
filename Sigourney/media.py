try:
    from flask import current_app as app, url_for
    import json
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

def find_thumbnail(video, thumbnails_directory):
    extensions = [".png", ".jpg", ".jpeg", ".svg"]
    thumbnails_directory = os.path.join(app.root_path, "static", thumbnails_directory)
    base_name = os.path.splitext(video)[0]

    for ext in extensions:
        thumbnail_file = f"{base_name}{ext}"
        full_path = os.path.join(thumbnails_directory, thumbnail_file)
        if os.path.isfile(full_path):
            return thumbnail_file

    return ""

def get_episodes(directory, thumbnails_directory, page=1, per_page=16):
    episodes = next(os.walk(directory))[2]
    episodes_metadata = [{
        "title": f"Series {directory.split('/')[-1]}",
        "breakdown": []
    }]

    episodes.sort()

    start = (page - 1) * per_page
    end = start + per_page
    paginated_episodes = episodes[start:end]

    for episode in paginated_episodes:
        thumbnail_file = find_thumbnail(episode, thumbnails_directory)
        thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
        thumbnail_url = url_for("static", filename=thumbnail_relative_path)

        episodes_metadata[0]["breakdown"].append({
            "thumbnail": thumbnail_url,
            "video": f"/{os.path.join(directory, episode)}"
        })

    return episodes_metadata

def get_films(directory, thumbnails_directory, page=1, per_page=10):
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
                thumbnail_file = find_thumbnail(show_folder, thumbnails_directory)
                thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
                thumbnail_url = url_for("static", filename=thumbnail_relative_path)

                shows_metadata.append({
                    "title": metadata.get("title"),
                    "thumbnail": thumbnail_url,
                    "video": os.path.join(directory, metadata.get("src"))
                })

    return shows_metadata

def get_series(directory, thumbnails_directory, page=1, per_page=32):
    series_count = 0
    metadata_path = os.path.join(directory, "metadata.json")

    if os.path.isfile(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            series_count = metadata.get("series")

    series_metadata = [{
        "title": metadata.get("title"),
        "breakdown": []
    }]

    for series in range(series_count):
        series_folder = os.path.join(directory, str(series + 1))

        thumbnail_file = find_thumbnail(str(series + 1), thumbnails_directory)
        thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
        thumbnail_url = url_for("static", filename=thumbnail_relative_path)

        series_metadata[0]["breakdown"].append({
            "title": f"Series {series + 1}",
            "thumbnail": thumbnail_url,
            "slug": f"{series_folder.split('static')[1]}"
        })
    
    return series_metadata

def get_tv_shows(directory, thumbnails_directory, page=1, per_page=32):
    absolute_directory = os.path.join(app.root_path, "static", directory)
    absolute_thumbnails_directory = os.path.join(app.root_path, "static", thumbnails_directory)

    shows = next(os.walk(absolute_directory))[1]
    shows_metadata = []

    shows = [show for show in shows if show != "category-thumbnails"]
    shows.sort()

    start = (page - 1) * per_page
    end = start + per_page
    paginated_shows = shows[start:end]

    for show_folder in paginated_shows:
        metadata_path = os.path.join(absolute_directory, show_folder, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                thumbnail_file = find_thumbnail(show_folder, absolute_thumbnails_directory)
                thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
                thumbnail_url = thumbnail_relative_path

                shows_metadata.append({
                    "title": metadata.get("title"),
                    "thumbnail": thumbnail_url,
                    "slug": f"/tv-shows/{show_folder}"
                })

    return shows_metadata

def is_image_file(filename):
    image_extensions = {'png', 'gif', 'jpg', 'jpeg'}
    return filename.split('.')[-1].lower() in image_extensions

def get_videos(directory, thumbnails_directory, page=1, per_page=32):
    start = (page - 1) * per_page
    end = start + per_page

    all_videos = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    videos = all_videos[start:end]

    video_thumbnail_pairs = []

    for video in videos:
        video_path = os.path.join(directory, video)
        is_image = is_image_file(video_path)
        if is_image:
            thumbnail_url = os.path.relpath(video_path, start=app.root_path)
        else:
            thumbnail_file = find_thumbnail(video, thumbnails_directory)
            thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
            thumbnail_url = os.path.relpath(thumbnail_relative_path, start=app.root_path)

        video_thumbnail_pairs.append({
            "video": os.path.relpath(video_path, start=app.root_path),
            "thumbnail": thumbnail_url,
            "is_image": is_image
        })

    return video_thumbnail_pairs