try:
    import smtplib
    import socket
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

def get_local_ip():
    try:
        # Connect to a remote server to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error: {e}"

def send_notification():
    sender_email = os.getenv("SENDER_MAIL_ADDRESS")
    receiver_email = os.getenv("RECIEVER_MAIL_ADDRESS")
    password = os.getenv("SENDER_MAIL_APP_PASSWORD")

    local_ip = get_local_ip()
    app_port = os.getenv("APP_PORT")

    body = (
        "The Media Server is now running. Click <a href='http://" + local_ip  + ":" + app_port  + "'>here</a> to open.<br><br>"
        "<strong style='color: #3B877B'>Sigourney</strong>"
    )

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Media server active"

    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(os.getenv("MAIL_HOST"), os.getenv("MAIL_PORT"))
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Notification sent successfully")
    except Exception as e:
        print(f"Error sending notification: {e}")
