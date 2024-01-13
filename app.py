import Sigourney as sigourney

try:
    import datetime
    from dotenv import load_dotenv
    from flask import Flask, render_template, request, url_for
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

app = Flask(__name__)

@app.route("/")
@sigourney.requires_auth
def index():
    visitor_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    visit_time = datetime.datetime.now()
    visit_logger.info(f"Visitor IP: {visitor_ip}, User-Agent: {user_agent}, Time: {visit_time}")

    return render_template("index.html", username=request.authorization.username)

@app.route("/films")
@sigourney.requires_auth
def films():
    return render_template("archive.html", title="Films")

@app.route("/tv")
@sigourney.requires_auth
def tv():
    return render_template("archive.html", title="TV Shows")

@app.route("/videos")
@sigourney.requires_auth
def videos():
    videos_directory = "videos"
    thumbnails_directory = "thumbnails/videos"
    video_thumbnail_pairs = sigourney.get_videos(videos_directory, thumbnails_directory, page=1)

    for pair in video_thumbnail_pairs:
        pair["video"] = url_for("static", filename=pair["video"])
        pair["thumbnail"] = url_for("static", filename=pair["thumbnail"])

    return render_template("archive.html", title="Videos", videos=video_thumbnail_pairs)

if __name__ == "__main__":
    load_dotenv()
    
    activity_logger = sigourney.start_logging_activity()
    visit_logger = sigourney.start_logging_visits()

    host_ip = os.getenv("APP_IP")
    host_port = os.getenv("APP_PORT")

    app.run(host=host_ip, port=host_port)