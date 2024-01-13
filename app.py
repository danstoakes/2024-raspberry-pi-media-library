import Sigourney as sigourney

try:
    import datetime
    from flask import Flask, render_template, request
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

app = Flask(__name__)

@app.route("/")
@sigourney.requires_auth
def index():
    visitor_ip = request.remote_addr
    visit_time = datetime.datetime.now()
    visit_logger.info(f"Visitor IP: {visitor_ip}, Time: {visit_time}")

    return render_template("index.html", username=request.authorization.username)

if __name__ == "__main__":
    activity_logger = sigourney.start_logging_activity()
    visit_logger = sigourney.start_logging_visits()
    app.run(host="0.0.0.0", port=6969)