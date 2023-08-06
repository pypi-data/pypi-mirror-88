import smtplib, ssl

def send_email(sender_email,receiver_email,password):
    '''smtplib and ssl to send email from gmail account'
       must be passed your email to send from, email to recieve at, and password of email account'''
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = """\
        Subject: Code done running

        Current cell has completed running"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
