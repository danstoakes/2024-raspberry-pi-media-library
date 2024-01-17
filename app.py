import Sigourney as sigourney

try:
    import datetime
    from dotenv import load_dotenv
    from flask import g, abort, Flask, send_from_directory, render_template, request
    import json
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

app = Flask(__name__)

@app.route("/")
@sigourney.requires_auth
@sigourney.set_super_flag
def index():
    visitor_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    visit_time = datetime.datetime.now()
    visit_logger.info(f"Visitor IP: {visitor_ip}, User-Agent: {user_agent}, Time: {visit_time}")

    return render_template("index.html", title="Home", is_super=g.is_super, password=os.getenv("SUPER_PASSWORD"))

@app.route("/films")
@sigourney.requires_auth
def films():
    directory = "static/films"
    thumbnails_directory = "thumbnails/films"
    films_metadata = sigourney.get_films(directory, thumbnails_directory, page=1)

    return render_template("archive.html", title="Films", videos=films_metadata)

@app.route("/tv-shows/<slug>")
@sigourney.requires_auth
def tv_show(slug):
    tv_show_directory = f"static/tv-shows/{slug}"
    thumbnails_directory = f"tv-shows/{slug}/series-thumbnails"
    series = sigourney.get_series(tv_show_directory, thumbnails_directory, page=1)

    return render_template("tv_landing_page.html", series=series[0]["breakdown"], title=series[0]["title"])

@app.route("/tv-shows/<slug>/<sub_slug>")
@sigourney.requires_auth
def tv_show_detail(slug, sub_slug):
    tv_show_directory = f"static/tv-shows/{slug}/{sub_slug}"
    thumbnails_directory = f"thumbnails/tv-shows/{slug}"
    episodes = sigourney.get_episodes(tv_show_directory, thumbnails_directory, page=1)

    return render_template("tv_details_page.html", episodes=episodes[0]["breakdown"], title=episodes[0]["title"])

@app.route("/tv-shows")
@sigourney.requires_auth
def tv_shows():
    tv_shows_directory = "static/tv-shows"
    thumbnails_directory = "thumbnails/tv-shows"
    shows_metadata = sigourney.get_tv_shows(tv_shows_directory, thumbnails_directory, page=1)

    return render_template("tv.html", title="TV", shows=shows_metadata)

@app.route("/videos")
@sigourney.requires_auth
def videos():
    videos_directory = "videos"
    thumbnails_directory = "thumbnails/videos"
    video_thumbnail_pairs = sigourney.get_videos(videos_directory, thumbnails_directory, page=1)

    return render_template("archive.html", title="Videos", videos=video_thumbnail_pairs)

@app.route("/locker")
@sigourney.requires_super
def locker():
    media_directory = "locker"
    thumbnails_directory = "thumbnails/locker"
    media_thumbnail_pairs = sigourney.get_videos(media_directory, thumbnails_directory, page=1, per_page=400)

    return render_template("locker.html", title="Locker", media=media_thumbnail_pairs)

@app.route('/static/locker/<path:filename>')
@sigourney.requires_super
def locker_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'locker'), filename)

@app.route('/static/films/<path:filename>')
@sigourney.requires_auth
def protected_films(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'films'), filename)

@app.route('/static/tv-shows/<path:filename>')
@sigourney.requires_auth
def protected_tv(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'tv-shows'), filename)

@app.route('/static/videos/<path:filename>')
@sigourney.requires_auth
def protected_videos(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'videos'), filename)

@app.route('/static/thumbnails/<path:filename>')
@sigourney.requires_auth
def protected_thumbnails(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'thumbnails'), filename)

if __name__ == "__main__":
    load_dotenv()
    
    activity_logger = sigourney.start_logging_activity()
    visit_logger = sigourney.start_logging_visits()

    host_ip = os.getenv("APP_IP")
    host_port = os.getenv("APP_PORT")

    app.run(host=host_ip, port=host_port)
