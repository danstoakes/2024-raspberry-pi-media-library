import Sigourney as sigourney
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

media_directory = os.path.join(BASE_DIR, "static", "locker")
thumbnails_directory = os.path.join(BASE_DIR, "static", "thumbnails", "locker")

sigourney.media.generate_thumbnails_for_all(media_directory, thumbnails_directory)