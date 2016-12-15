#! /usr/bin/python3

import os


from platform import node
from requests import get
from requests.exceptions import RequestException


from subprocess import run,check_output, PIPE, STDOUT, CalledProcessError
from argparse import ArgumentParser
from jinja2 import Template, FileSystemLoader, Environment
from sys import exit
from smtplib import SMTP
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def send_mail(data,repicient):

    user        = '<hidden>'
    password    = '<hidden>'
    header_from = '<hidden>' 
    header_subj = 'ClamAV scan report'

    msg = MIMEMultipart()
    msg['From']    = user
    msg['To']      = repicient
    msg['Subject'] = "[{0}] ClamAV: scanned {1} on {2} ({3})".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), parser.parse_args().dir, node(), get_ip())

    msg.attach(MIMEText(data,'html'))

    client = SMTP(host='smtp.office365.com', port=587)
    client.starttls()
    client.login(user,password)

    client.sendmail(header_from,repicient,msg.as_string())
    client.quit()


def get_ip():
    try:
        return get('https://api.ipify.org').text
    except RequestException:
        return '0.0.0.0'

parser = ArgumentParser(description = "ClamAV Scanner. Example: ./scan.py '/root' 'billgates@microsoft.com' ")
parser.add_argument('dir',type = str,help = 'Directory to scan')
parser.add_argument('sendto',type = str, help = 'Report repicient address')

data = []
if parser.parse_args().dir:
    try:
        for line in run(['clamscan','-r','-i','--no-summary','{}'.format(parser.parse_args().dir)], stdout=PIPE).stdout.decode('utf-8').split('\n'):
            if line: data.append( ''.join(line.split()[0:2]).split(':')  )
    except OSError:
         print("Please check clamav is installed or present in PATH") 
         pass
# Should not happen anyway since argparse protects me
elif not parser.parse_args().dir or not parser.parse_args().sendto:
    print("No directory or repicient is given. Please check. Help: scan.py -h. Exiting...")
    exit(1)

loader   = FileSystemLoader( os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates') )
env      = Environment(loader=loader, trim_blocks = True, lstrip_blocks = True)
template = env.get_template('report.tmpl')

if data:
    rendered_html = (template.render(data = {
                                             'data':data,
                                             'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                             'dir':parser.parse_args().dir,
                                             'host':node(),
                                             'ip':get_ip()
                                            }))
    send_mail(rendered_html, repicient=parser.parse_args().sendto)

