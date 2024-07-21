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
        thumbnail_url = os.path.relpath(thumbnail_relative_path, start=app.root_path)

        metadata_path = os.path.join(directory, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)

        for item in metadata:
            if item["src"] == episode:
                episodes_metadata[0]["breakdown"].append({
                    "thumbnail": f"/static{thumbnail_url.split('static')[1]}",
                    "video": f"/static{os.path.join(directory.split('static')[1], episode)}",
                    "title": item.get("title"),
                    "src": item.get("src")
                })
                break

    episodes_metadata_sorted = sorted(episodes_metadata, key=lambda x: x["title"])

    return episodes_metadata_sorted

def get_films(directory, thumbnails_directory, page=1, per_page=32):
    # Get list of films excluding 'category-thumbnails'
    films = [film for film in next(os.walk(directory))[1] if film != "category-thumbnails"]
    
    # Sort films alphabetically
    films.sort()
    
    # Calculate start and end indices for pagination
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get the paginated films
    paginated_films = films[start:end]
    
    films_metadata = []

    for film_folder in paginated_films:
        metadata_path = os.path.join(directory, film_folder, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                thumbnail_file = find_thumbnail(film_folder, thumbnails_directory)
                thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
                thumbnail_url = os.path.relpath(thumbnail_relative_path, start=app.root_path)

                films_metadata.append({
                    "title": metadata.get("title"),
                    "thumbnail": thumbnail_url,
                    "video": f"/static{os.path.join(directory.split('static')[1], metadata.get('src'))}"
                })
    
    # Calculate total pages
    total_films = len(films)
    total_pages = (total_films + per_page - 1) // per_page

    return {
        "films": films_metadata,
        "page": page,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages
    }

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
        thumbnail_url = os.path.relpath(thumbnail_relative_path, start=app.root_path)

        series_metadata[0]["breakdown"].append({
            "title": f"Series {series + 1}",
            "thumbnail": f"/static{thumbnail_url.split('static')[1]}",
            "slug": f"{series_folder.split('static')[1]}"
        })
    
    return series_metadata

def get_tv_shows(directory, thumbnails_directory, page=1, per_page=32):
    # Get list of shows excluding 'category-thumbnails'
    shows = [show for show in next(os.walk(directory))[1] if show != "category-thumbnails"]
    
    # Sort shows alphabetically
    shows.sort()
    
    # Calculate start and end indices for pagination
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get the paginated shows
    paginated_shows = shows[start:end]
    
    shows_metadata = []

    for show_folder in paginated_shows:
        metadata_path = os.path.join(directory, show_folder, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                thumbnail_file = find_thumbnail(show_folder, thumbnails_directory)
                thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
                thumbnail_url = os.path.relpath(thumbnail_relative_path, start=app.root_path)

                shows_metadata.append({
                    "title": metadata.get("title"),
                    "thumbnail": thumbnail_url,
                    "slug": f"/tv-shows/{show_folder}"
                })
    
    # Calculate total pages
    total_shows = len(shows)
    total_pages = (total_shows + per_page - 1) // per_page

    return {
        "shows": shows_metadata,
        "page": page,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages
    }

def is_image_file(filename):
    image_extensions = {'png', 'gif', 'jpg', 'jpeg'}
    return filename.split('.')[-1].lower() in image_extensions

import os

def get_videos(directory, thumbnails_directory, page=1, per_page=32):
    # Calculate start and end indices for pagination
    start = (page - 1) * per_page
    end = start + per_page

    # List all files in the directory
    all_files = os.listdir(directory)
    all_videos = [f for f in all_files if os.path.isfile(os.path.join(directory, f))]

    # Calculate total pages
    total_videos = len(all_videos)
    total_pages = (total_videos + per_page - 1) // per_page

    # Get the videos for the current page
    videos = all_videos[start:end]

    video_thumbnail_pairs = []

    for video in videos:
        video_path = os.path.join(directory, video)
        is_image = is_image_file(video_path)
        if is_image:
            thumbnail_url = os.path.relpath(video_path, start=app.root_path)
        else:
            thumbnail_file = find_thumbnail(video, thumbnails_directory)
            if thumbnail_file:
                thumbnail_relative_path = os.path.join(thumbnails_directory, thumbnail_file)
                thumbnail_url = os.path.relpath(thumbnail_relative_path, start=app.root_path)
            else:
                thumbnail_url = None  # Handle case where thumbnail is not found

        video_thumbnail_pairs.append({
            "video": os.path.relpath(video_path, start=app.root_path),
            "thumbnail": thumbnail_url,
            "is_image": is_image
        })

    return {
        "videos": video_thumbnail_pairs,
        "page": page,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages
    }
