try:
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