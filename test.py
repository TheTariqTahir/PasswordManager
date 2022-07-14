import smtplib
sent_from = "dev.tariqtahir@gmail.com"

to ='thetariqtahir43@gmail.com'
subject = 'Password Reset'
link="link"

email_text = """\
From: %s
To: %s
Subject: %s

Hi,

Please click on below link to reset your password for PasswordManager App.

%s

Thanks for using App

Regards
M. Tariq
Ph# +923040755464


""" % (sent_from, ", ".join(to), subject,link)



try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('dev.tariqtahir@gmail.com','xmwaqkujwczlrxvm')
    server.sendmail(sent_from, to, email_text)
    server.close()
except:
    print('Something went wrong...')

# server.login('dev.tariqtahir@gmail.com','xmwaqkujwczlrxvm')