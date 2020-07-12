from itsdangerous import URLSafeTimedSerializer
from config import app
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'briankathukya2000@gmail.com'
password = 'ddigjvmnffdurpct'

def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(email,salt=app.config['SECURITY_PASSWORD_SALT'])
    
def confirm_token(token,expiration=300):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age = expiration
        )
    except:
        return False
    return email

def send_mail(subject,receiver_email,body):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    html = body
    htmlattach = MIMEText(html,'html')
    message.attach(htmlattach)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(
            sender_email,receiver_email,message.as_string()
        )
