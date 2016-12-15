#! /usr/bin/python3

import os
from sys import exit
from platform import node
from datetime import datetime
from subprocess import run, check_output, PIPE, STDOUT, CalledProcessError
from argparse import ArgumentParser
from jinja2 import Template, FileSystemLoader, Environment
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

parser = ArgumentParser(description="ClamAV Scanner. Example: ./scan.py '/root' 'billgates@microsoft.com' ")
parser.add_argument('dir', type=str, help='Directory to scan')
parser.add_argument('sendto', type=str, help='Report recipient address')

_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
_dir = parser.parse_args().dir
_recipient = parser.parse_args().sendto
_host = node()


def send_mail(html, recipient):
    user = '<hidden>'
    password = '<hidden>'
    header_from = '<hidden>'

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = "[{0}] ClamAV: scanned {1} on {2}".format(_now, _dir, _host)

    msg.attach(MIMEText(html, 'html'))

    client = SMTP(host='smtp.office365.com', port=587)
    client.starttls()
    client.login(user, password)

    client.sendmail(header_from, recipient, msg.as_string())
    client.quit()


data = []

try:
    for line in run(['clamscan', '-r', '-i', '--no-summary', '{}'.format(_dir)], stdout=PIPE).stdout.decode(
            'utf-8').split('\n'):
        if line:
            data.append(''.join(line.split()[0:2]).split(':'))
except OSError:
    print("Please check ClamAV is installed or present in PATH")
    exit(1)

loader = FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template('report.tmpl')

if data:
    rendered_html = (template.render(data={
        'data': data,
        'time': _now,
        'dir': _dir,
        'host': _host
    }))
    send_mail(rendered_html, recipient=_recipient)
