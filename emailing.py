from smtplib import SMTP
from email.message import EmailMessage
from imghdr import what
from os import getenv

sender = getenv("EMAIL")
password = getenv("PASSWORD")


def send_email(image_path):
    message = EmailMessage()
    message["Subject"] = "An object has entered the frame"
    message.set_content("Hey, the script detected a new object entering the frame.")

    with open(image_path, "rb") as file:
        content = file.read()

    message.add_attachment(content, maintype="image", subtype=what(None, content))

    gmail = SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, sender, message.as_string())
    gmail.quit()
