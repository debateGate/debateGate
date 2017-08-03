"""
Contains all non-web-development-specific functions.
"""
import smtplib
from threading import Thread

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.main import main


def send_email(msgArr, receiver_email):
    with main.app_context():
        thr = Thread(target=email_synchronous_process, args=[msgArr, receiver_email])
        thr.start()


def email_synchronous_process(msgArr, receiver_email):
    sender = main.config["ADDRESS"]
    receiver = receiver_email

    msg = MIMEMultipart('alternative')

    msg['Subject'] = msgArr[0]
    msg['From'] = sender
    msg['To'] = receiver

    html = msgArr[1]
    text = msgArr[2]

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

   # last part -- the html -- is preferred
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, main.config["PASSWORD"])
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    pass


def paginate_list(seq, step):
    for start in range(0, len(seq), step):
        yield seq[start:start+step]
