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


def send_mail(html, recipient, subject):
    user = '<hidden>'
    password = '<hidden>'
    header_from = '<hidden>'

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(html, 'html'))

    client = SMTP(host='smtp.office365.com', port=587)
    client.starttls()
    client.login(user, password)

    client.sendmail(header_from, recipient, msg.as_string())
    client.quit()


def parse_clamav(parsed_args_p):
    data = []

    try:
        for line in run(['clamscan', '-r', '-i', '--no-summary', '{}'.format(parsed_args_p.dir)],
                        stdout=PIPE).stdout.decode('utf-8').split('\n'):
            if line:
                data.append(''.join(line.split()[0:2]).split(':'))
    except OSError:
        print("Please check ClamAV is installed or present in PATH")
        exit(1)

    if not data:
        sys.exit(0)

    return data


def form_template(data, parsed_args_t, now_t, host_t):

    loader = FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('report.tmpl')

    rendered_html = (template.render(data={
        'data': data,
        'time': now_t,
        'dir': parsed_args_t.dir,
        'host': host_t
    }))

    return rendered_html


if __name__ == "__main__":
    parser = ArgumentParser(description="ClamAV Scanner. Example: ./scan.py '/root' 'billgates@microsoft.com' ")
    parser.add_argument('dir', type=str, help='Directory to scan')
    parser.add_argument('sendto', type=str, help='Report recipient address')
    parsed_args = parser.parse_args()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    host = node()

    send_mail(form_template(parse_clamav(parsed_args), parsed_args, now, host), recipient=parsed_args.sendto,
              subject="[{0}] ClamAV: scanned {1} on {2}".format(now, parsed_args.dir, host))
