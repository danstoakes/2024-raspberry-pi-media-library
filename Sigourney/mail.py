try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os
except ImportError as error:
    print("Some or all of the necessary packages to run the script are missing. Please consult the README for instructions on how to install them.")
    print(f"Original error: {error}")
    exit(1)

def send_notification():
    sender_email = os.getenv("SENDER_MAIL_ADDRESS")
    receiver_email = os.getenv("RECIEVER_MAIL_ADDRESS")
    password = os.getenv("SENDER_MAIL_APP_PASSWORD")

    body = "The Media Server has been started."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Sigourney Media Server Active"

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(os.getenv("MAIL_HOST"), os.getenv("MAIL_PORT"))
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Notification sent successfully")
    except Exception as e:
        print(f"Error sending notification: {e}")