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
