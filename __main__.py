import Sigourney as sigourney

try:
    from flask import Flask, render_template, request
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

app = Flask(__name__)

@app.route("/")
@sigourney.requires_auth
def index():
    return render_template("index.html", username=request.authorization.username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)