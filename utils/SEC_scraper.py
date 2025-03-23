"""
util script to get:
10k filing reports
company metadata
company fact

output will be JSON data structures

Notes:

data.sec.gov hosts an API that provides JSON data, free access (no auth, no API key)
The filers provide submissions

The API includes submission history by filers and the XBRL (eXtensible Business Reporting Language) data from financial statements (forms 10-Q, 10-K, 8-K, 20-F, 40-F, 6-K, and their variants)

API also provides bulk ZIP files for all JSON structures

Unique identifier for filers: Central Index Key (CIK)

"""

import requests
import dotenv
import os

import json

from pprint import pprint

endpoints = {
    "submissions": "https://data.sec.gov/submissions",
    "companyconcept": "https://data.sec.gov/api/xbrl/companyconcept",
    "companyfacts": "https://data.sec.gov/api/xbrl/companyfacts"
}
dotenv.load_dotenv()
email = os.environ.get(key="email")
# EDGAR fair access policy requires declaration of user-agent to prevent botnets
header = {"User-Agent": email}

def foramt_cik(cik):
    cik = str(cik).zfill(10)
    return cik

def get_submissions(company):
    cik = company["cik_str"]
    cik = foramt_cik(cik)
    filing_metadata = requests.get(
        url=f"{endpoints["submissions"]}/CIK{cik}.json",
        headers=header
    )
    
    return filing_metadata

# get the ticker to CIK mapping
# tickers = requests.get(
#     url="https://www.sec.gov/files/company_tickers.json",
#     headers=header
# )

with open("data/company_tickers.json", 'r') as f:
    s = f.read()
    tickers = json.loads(s=s)

# pick the first company for test run
test_company = tickers["0"]

metadata = get_submissions(test_company)

pprint(metadata.json().keys())
# pprint(metadata.json())
