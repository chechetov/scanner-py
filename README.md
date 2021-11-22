### This is a little scanner script

It scans files for viruses using ClamAV and VirusTotal public API.

Installation:

1. Clone the repository to target server
2. Install dependencies using ```pip3 install -r requirements.txt```
3. Install ClamAV using ```apt-get install clamav```
4. Add e-mail and password to configuration file

Usage:

```./python3 scan.py /path-to-scan/ recipient@e-mail.com```

Once scan is completed, recipient will get a report via e-mail.

Notes:

Scan may take a significant amount of time.

In case of doubts, please check if ClamAV is still running with ```ps aux | grep clamav```

Also, ```scan.log``` may be checked in order to see what stage of execution is currently performed.
