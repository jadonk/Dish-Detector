import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
img = open("/var/lib/cloud9/Dish-Detector/camera-test.jpg", "rb")
msg = MIMEMultipart()
msg.attach(MIMEImage(img.read()))
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login('jkridner@gmail.com', 'ftyaxfcbnbljpkjf')
server.sendmail('jkridner@gmail.com', '5867641992@mms.att.net', msg.as_string())
