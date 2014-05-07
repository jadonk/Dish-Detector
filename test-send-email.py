import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
img = open("/var/lib/cloud9/Dish-Detector/camera-test.jpg", "rb")
msg = MIMEMultipart()
msg.attach(MIMEImage(img.read()))
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login('user@gmail.com', 'password')
server.sendmail('user@gmail.com', '2125555555@mms.att.net', msg.as_string())
