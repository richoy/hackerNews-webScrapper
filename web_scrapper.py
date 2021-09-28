from email.mime import text
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import argparse

"""
This scripts is a web scrapper of https://news.ycombinator.com that
gets the results of the main page and send them to the provided
email.

Currently working with Gmail

"""

# Parser creation
parser = argparse.ArgumentParser(prog='scr',
                                 description='Hacker news scrapper that sends an email with latest news')
parser.add_argument('-f',
                    '--fromemail',
                    action='store')
parser.add_argument('-t',
                    '--to',
                    action='store')
parser.add_argument('-p',
                    '--password',
                    action='store')

args = parser.parse_args()

# Email configuration, edit this with your desired values
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = 'placeholder@gmail.com'
TO = 'placeholder@gmail.com'
PASS = '12345'

# Change values if arguments are provided on the command line
if args.fromemail is not None:
    FROM = args.fromemail

if args.to is not None:
    TO = args.to

if args.password is not None:
    PASS = args.password

# Get current date and time for email timestamp
now = datetime.datetime.now()

# Email content placeholder

content = ''

# Extracting Hacker News Stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories: </b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')

    return(cnt)

cnt = extract_news('https://news.ycombinator.com')
content += cnt
content += ('<br>---------<br>')
content += ('<br><br>End of Message')

print('Composing Email...')


# Email body
msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

# Attacha email body
msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')
server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1) # 0 for no messages
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
