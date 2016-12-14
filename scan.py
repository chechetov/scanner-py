#! /usr/bin/python3

import os

from subprocess import run,check_output, PIPE, STDOUT, CalledProcessError
from argparse import ArgumentParser
from jinja2 import Template, FileSystemLoader, Environment
from sys import exit
from smtplib import SMTP
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_mail(file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'report.html'),repicient='<hidden>'):

    user        = '<hidden>'
    password    = '<hidden>'
    header_from = '<hidden>' 
    header_subj = 'ClamAV scan report'

    msg = MIMEMultipart()
    msg['From']    = user
    msg['To']      = repicient
    msg['Subject'] = header_subj
    attach = MIMEBase('application','octet-stream')

    with open(file_path, mode = 'r') as file_obj:
        attach.set_payload(file_obj.read())

    encoders.encode_base64(attach)
    attach.add_header('Content-Disposition', "attachment; filename = report.html")
    msg.attach(attach)

    client = SMTP(host='smtp.office365.com', port=587)
    client.starttls()
    client.login(user,password)

    client.sendmail(header_from,repicient,msg.as_string())
    client.quit()

parser = ArgumentParser(description = "Input params: directory to scan. Launch example: ./scan.py --dir '/root' ")
parser.add_argument('--dir',type = str,help = 'directory to scan')
parser.add_argument('--sendto',type = str, help = 'report repicient address')

data = []

if parser.parse_args().dir:
    try:
        for line in run(['clamscan','-r','-i','--no-summary','{}'.format(parser.parse_args().dir)], stdout=PIPE).stdout.decode('utf-8').split('\n'):
            if line: data.append( ''.join(line.split()[0:2]).split(':')  )
    except OSError:
         print("Please check clamav is installed or present in PATH") 
         pass
else:
    print("No directory is given. Please provide me with --dir. Exiting...")
    exit(1)

loader   = FileSystemLoader( os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates') )
env      = Environment(loader=loader, trim_blocks = True, lstrip_blocks = True)
template = env.get_template('report.tmpl')

if data:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'report.html'), mode='w',encoding='utf8') as report_file:
        report_file.write(template.render( data = { 'data':data,'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'dir':parser.parse_args().dir }))
    send_mail(repicient=parser.parse_args().sendto)

