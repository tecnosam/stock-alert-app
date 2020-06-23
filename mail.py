import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'ikabolo59'
PASSWORD = 'ikechukwu1023'

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    # message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(MY_ADDRESS, PASSWORD)

    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        # message = message_template.substitute(PERSON_NAME=name.title())
        message = f"Testing mailing service {name}"

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST"
    
        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg
    s.quit()
    
if __name__ == '__main__':
    main()