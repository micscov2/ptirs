import smtplib
import getpass
from orm_file import Secret, User

def send_email(user_name, ptir_id, description):
    print "Start sending email now"
    email = User.objects(name=user_name)[0].email
    msg = "Subject: PTIR Created\n\n{} - {}".format(ptir_id, description)
    send_to = email
    username = "micscov2@gmail.com"
    print("send email to {}, ptir_id {}, msg: {}".format(email, ptir_id, msg))
    passwd = "***"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, passwd)
    server.sendmail(username, send_to, msg)
    server.quit()
    print "Email sent!!"
