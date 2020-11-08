import smtplib

def send_mail(email, url):

    
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('goshigo23@gmail.com', 'bdryaouqjwrdoape')
    except:
        print('Error!!!!')

    subject = 'Price fell down!'
    body = f"Check your product link: {url}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('goshigo23@gmail.com', email, msg)
    print('Email has been sent')
    server.quit()

