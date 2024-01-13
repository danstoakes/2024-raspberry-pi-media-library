try:
    from flask import request, Response
    from functools import wraps
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

def check_auth(username, password):
    return username == os.getenv("AUTH_USERNAME") and password == os.getenv("AUTH_PASSWORD")

def authenticate():
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials", 401, 
        {"WWW-Authenticate": "Basic realm='Login Required'"}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
