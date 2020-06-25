from threading import Thread
import sys, os, math
import requests
from api import fetch_user_data, compute_activated
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_simple_message(msg, recv, recv_email):
    	return requests.post(
		"https://api.mailgun.net/v3/sandbox3cc88e9992e249a2af4775be86df605e.mailgun.org/messages",
		auth=("api", "2c20989f75117fdea19a0e2866beb72e-1b6eb03d-5b6a4edc"),
		data={"from": "OPENSTOCK's Mailgun <postmaster@sandbox3cc88e9992e249a2af4775be86df605e.mailgun.org>",
			"to": f"{recv} <{recv_email}>",
			"subject": "Stock Alert",
			"text": msg})

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


class Notification:
    def __init__(self):
        self.MY_ADDRESS = 'ikabolo59'
        self.PASSWORD = 'ikechukwu1023'
        self.s = smtplib.SMTP_SSL('smtp.gmail.com')
        self.s.login(self.MY_ADDRESS, self.PASSWORD)
    def ping(self, email):
        pass
    def bulk(self, uids, symbol, theme = "trade"):
        message_template = read_template(f'templates/themes/txt/{theme}.txt')

        # set up the SMTP server

        for uid in uids:
            dat = fetch_user_data( uid[0] )
            if ( compute_activated( dat[4] ) != True ):
                continue
            msg = MIMEMultipart()
            # create a message
            message = message_template.substitute(name=dat[1].title(), symbol = symbol)

            # setup the parameters of the message
            msg['From']="Abolo Samuel <%s>" % self.MY_ADDRESS
            msg['To']=dat[2]
            msg['Subject']= f"Alert from OPENSTOCK"
        
            msg.attach(MIMEText(message, 'plain'))
            # th = Thread(target = self.s.send_message, args = [msg])
            # th.start()
            th = Thread(target = send_simple_message, args = (message, dat[1], dat[2]))
            th.start()
            print("Sending...")
            del msg
        # self.s.quit()
    