### This is a little scanner script

It scans files for viruses using ClamAV and VirusTotal public API.

Installation:

1. Clone the repository to target server
2. Install dependencies using ```pip3 install -r requirements.txt```
3. Install ClamAV using ```apt-get install clamav```
4. Add e-mail password to configuration file

Usage:

```./python3 scan.py /path-to-scan/ recipient@e-mail.com```

Once scan is completed, recipient will get a report via e-mail.
