# coding=utf-8
import csv
import re
from datetime import datetime
from ledger.entry import Entry
import curses

def read_csv(csv_file, ledger_file):
    read_ledger_accounts(ledger_file)

    f = open(csv_file)
    reader = csv.reader(f, delimiter='\t')

    entries = []
    for k in reader:
        entry = Entry()
        entry.date = datetime.strptime(k[2], "%Y%m%d").strftime('%Y/%m/%d')
        entry.amount = float(k[6].replace(",", "."))
        entry.description = k[7]
        entries.append(entry)

    return entries

def complete_entries(buffer, entries):
    """
    @entries Entry[]
    """
    for entry in entries:
        buffer.writeln("Description: {}".format(entry.description))
        buffer.writeln("Date: {}".format(entry.date))
        buffer.writeln("Amount: {}".format(entry.amount))

        action = buffer.input_chr("Action ((E)dit description, (S)ave) > ")

        if action == "e":
            buffer.write("Description: ")
            #entry.description = buffer.getstr()

        if entry.amount > 0:
            prompt = "Account to (income): "
        else:
            prompt = "Account to (expense): "

        entry.account_to.append(buffer.input(prompt))
        entry.account_from.append(buffer.input("Account from: "))

def read_ledger_accounts(path):
    f = open(path)

    accounts = {}
    account_pattern = re.compile('([a-zA-Z:]+)\s+€[-0-9.]+')

    for line in f:
        matches = account_pattern.findall(line)
        if matches:
            account = matches[0]
            accounts = parse_account(account, accounts)

#    write(json.dumps(accounts, indent=4))


def parse_account(account, accounts):
    subaccounts = account.split(":")
    current_account = accounts
    for subaccount in subaccounts:
        if not subaccount in current_account:
            current_account[subaccount] = {}
        current_account = current_account[subaccount]

    return accounts

