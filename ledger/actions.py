# coding=utf-8
import csv
import re
from datetime import datetime
from ledger.entry import Entry
from decimal import Decimal

def read_csv(csv_file):

    f = open(csv_file)
    reader = csv.reader(f, delimiter='\t')

    entries = []
    for k in reader:
        entry = Entry()
        entry.date = datetime.strptime(k[2], "%Y%m%d").strftime('%Y/%m/%d')
        entry.amount = Decimal(k[6].replace(",", "."))
        entry.description = k[7]
        entries.append(entry)

    return entries

def read_ledger_accounts(path):
    f = open(path)

    accounts = set()
    account_pattern = re.compile('\s{4}([a-zA-Z:]+)')

    for line in f:
        matches = account_pattern.findall(line)
        if matches:
            account = matches[0]
            accounts.add(account)
            for parent_account in get_parent_accounts(account):
                accounts.add(parent_account)

    return accounts

def get_parent_accounts(account):
    parts = account.split(":")[:-1]
    parent_accounts = []
    for i in range(len(parts), 0, -1):
        parent_accounts.append(":".join(parts[:i]))
    return parent_accounts
