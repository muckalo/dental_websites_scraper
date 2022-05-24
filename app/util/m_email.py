from app.config.config import NOTIFICATION_EMAIL_FROM, NOTIFICATION_EMAIL_PASSWORD, NOTIFICATION_EMAIL_TO
import smtplib
from email.mime.text import MIMEText


def task_send_email(email_subject, email_msg):
    def send_email(**kwargs):
        try:
            email_from = kwargs["email_from"]
            email_pwd = kwargs["email_pwd"]
            email_to = kwargs["email_to"]
        except Exception as e:
            return "Email credentials failed: {}".format(e)

        try:
            email_msg = kwargs["email_msg"]
        except:
            email_msg = None

        try:
            email_subject = kwargs["email_subject"]
        except:
            email_subject = None

        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(email_from, email_pwd)

            m = MIMEText(email_msg)
            m['Subject'] = email_subject
            m['From'] = email_from
            m['To'] = email_to

            mail.sendmail(email_from, email_to, m.as_string())
            mail.close()

        except Exception as e:
            return "Send email failed: {}".format(e)

        return False

    """ SET CREDENTIALS AND EMAIL CONTENT """
    email_data = {
        "email_from": NOTIFICATION_EMAIL_FROM,
        "email_pwd": NOTIFICATION_EMAIL_PASSWORD,
        "email_to": NOTIFICATION_EMAIL_TO,
        "email_subject": email_subject,
        "email_msg": email_msg
    }

    """ SEND EMAIL """
    email_err = send_email(**email_data)
    if email_err:
        print(email_err)
