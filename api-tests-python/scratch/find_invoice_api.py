"""
Find all invoice and accountant related API endpoints and functions
from Angular bundles and downloaded scripts.
"""
import os, sys, re, json
sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import urllib3
urllib3.disable_warnings()
from config import Config
from client.api_client import BayMaxApiClient

client = BayMaxApiClient(Config.BASE_URL)
client.login(Config.USERNAME, Config.PASSWORD)

# 1. Check all endpoints in accountant and patient-accounts
probes = [
    # accountant
    "/api/accountant/invoices",
    "/api/accountant/registered-invoices",
    "/api/accountant/unregistered-invoices",
    "/api/accountant/reservations",
    "/api/accountant/reservations/open",
    "/api/accountant/leaving-requests",
    "/api/accountant/leaving-approval",
    "/api/accountant/payments",
    "/api/accountant/receipts",
    "/api/accountant/patient-debts",
    "/api/accountant/treasury",
    # invoice
    "/api/invoices",
    "/api/invoices/registered",
    "/api/invoices/unregistered",
    "/api/invoices/search",
    "/api/invoices/12780",
    "/api/invoice-details/12780",
    # patient account
    "/api/patient-accounts/12780",
    "/api/patient-accounts/reservations",
    "/api/patient-accounts/invoices",
    "/api/patient-accounts/invoices/12780",
    # ipd
    "/api/ipd/invoices",
    "/api/ipd/reservations",
    "/api/ipd/package-invoices",
    # treasury
    "/api/treasury/receipts",
    "/api/treasury/payment-orders",
    # discounts
    "/api/discounts",
    "/api/reservations/12780",
]

print("="*60)
print("TESTING PROBABLE ACCOUNTANT / INVOICE ENDPOINTS:")
print("="*60)
for p in probes:
    try:
        r = client.get(p)
        print(f"GET  {p:<45} -> {r.status_code}")
    except Exception as e:
        print(f"GET  {p:<45} -> ERROR {e}")

