try:
    import os
    import logging
    from logging.handlers import RotatingFileHandler
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

log_directory = os.path.join(os.path.dirname(__file__), "logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

def start_logging_activity():
    log_file_path = os.path.join(log_directory, "activity.log")

    activity_logger = logging.getLogger("ActivityLogger")
    activity_logger.setLevel(logging.INFO)
    activity_handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    activity_handler.setFormatter(formatter)

    if not activity_logger.handlers:
        activity_logger.addHandler(activity_handler)

    return activity_logger

def start_logging_visits():
    log_file_path = os.path.join(log_directory, "visits.log")

    visit_logger = logging.getLogger("VisitLogger")
    visit_logger.setLevel(logging.INFO)
    visit_handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    visit_handler.setFormatter(formatter)

    if not visit_logger.handlers:
        visit_logger.addHandler(visit_handler)

    return visit_logger