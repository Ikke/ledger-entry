# coding=utf-8
import csv
import re
from datetime import datetime
from ledger.entry import Entry
import curses

def read_csv(csv_file):

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

def complete_entries(entries, accounts, buffer):
    """
    @entries Entry[]
    """

    index = 0
    max = len(entries)
    while index < max:
        entry = entries[index]
        buffer.writeln(str(entry))

        action = buffer.input_chr("Action ((E)dit description, Set (A)ccounts, (S)ave) > ")

        if action == "s":
            if not entry.account_from or not entry.account_to:
                confirm = buffer.input_chr("Account information not complete. Still want to edit? (Y/n) ")
                if confirm != "n":
                    action = "a"
                else:
                    index += 1
            else:
                index += 1

        if action == "e":
            entry.description = buffer.input("Description: ")
        if action == "a":
            if entry.amount > 0:
                prompt = "Account to (income): "
            else:
                prompt = "Account to (expense): "

            entry.account_to = prompt_account(prompt, buffer, accounts)
            entry.account_from = prompt_account("Account from: ", buffer, accounts)
        buffer.writeln()

    return entries

def prompt_account(prompt, buffer, accounts):
    account_response = buffer.input(prompt)

    if account_response.isdigit():
        tmp_account = accounts[int(account_response)]
        buffer.write(prompt + tmp_account + ":")
        account_part = buffer.input()

        if account_part != "":
            tmp_account += ":" + account_part
    else:
        tmp_account = account_response

    accounts.add_account(tmp_account)
    return tmp_account

def read_ledger_accounts(path):
    f = open(path)

    accounts = set()
    account_pattern = re.compile('([a-zA-Z:]+)\s+€[-0-9.]+')

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
