#! /usr/bin/python3

from subprocess import run, PIPE
from argparse import ArgumentParser
from jinja2 import Template, FileSystemLoader, Environment
from sys import exit

import os

from datetime import datetime


parser = ArgumentParser(description = "Input params: directory to scan. Launch example: ./scan.py --dir '/root' ")
parser.add_argument('--dir',type = str,help = 'directory to scan')

data = []

if parser.parse_args().dir:
    for line in run(["clamscan -r -i --no-summary {}".format(parser.parse_args().dir)], shell=True, stdout=PIPE).stdout.decode('utf-8').split('\n'):
        if line: data.append( ''.join(line.split()[0:2]).split(':')  )
else:
    print("No directory is given. Please provide me with --dir. Exiting...") 
    exit(1)

loader   = FileSystemLoader( os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates') )
env      = Environment(loader=loader, trim_blocks = True, lstrip_blocks = True)
template = env.get_template('report.tmpl')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'report.html'), mode='w') as report_file:
    report_file.write(template.render(data={'data':data,'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}))
