import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Mailer:

    def __init__(self):
        self.strFrom = ""
        self.strTo = ""
        self.pwd = ""

    def send_message(self,fileName):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = "QR Code Mobile Pass"
        msgRoot['From'] = self.strFrom
        msgRoot['To'] = self.strTo

        # Create the body of the message.
        html = """\
            <p>Keep the QR code secure<br/>
                <img src="cid:image1">
            </p>
        """

        # Record the MIME types.
        msgHtml = MIMEText(html, 'html')
        img = open(fileName+'.png', 'rb').read()
        msgImg = MIMEImage(img, 'png')
        msgImg.add_header('Content-ID', '<image1>')
        msgImg.add_header('Content-Disposition', 'inline', filename=fileName+'.png')
        msgRoot.attach(msgHtml)
        msgRoot.attach(msgImg)

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.login(self.strFrom, self.pwd)
        s.set_debuglevel(1)
        s.sendmail(self.strFrom, self.strTo, msgRoot.as_string())
        s.quit()