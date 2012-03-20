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

def complete_entries(entries, accounts, buffer):
    """
    @entries Entry[]
    """

    account_from = prompt_account("Default account from: ", buffer, accounts)

    index = 0
    max = len(entries)
    while index < max:
        entry = entries[index]

        buffer.scroll_top()
        buffer.writeln("Entry {} of {}\n".format(index + 1, max))

        buffer.writeln(str(entry))

        action = buffer.input_chr("Action ((E)dit description, Set (A)ccounts, S(P)lit, (S)ave) > ")

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
            entry.account_from = account_from

        if action == "p":
            nr_of_statements = int(buffer.input("How many statements? "))
            amount_left = entry.amount
            entry.amount = Decimal(buffer.input("Amount for statement 1: "))
            amount_left -= entry.amount
            for i in range(1, nr_of_statements):
                new_entry = Entry()
                new_entry.amount = Decimal(buffer.input("Amount of statement {} ({} left): ".format(i+1, amount_left)))
                new_entry.date = entry.date
                amount_left -= new_entry.amount
                entries.insert(index+i, new_entry)
                max += nr_of_statements - 2

        buffer.writeln()

    return entries

def prompt_account(prompt, buffer, accounts):
    account_response = buffer.input(prompt)

    if account_response.isdigit():
        nr = int(account_response)
        if nr < len(accounts):
            tmp_account = accounts[int(account_response)]
            buffer.write(prompt + tmp_account + ":")
            account_part = buffer.input()

            if account_part != "":
                tmp_account += ":" + account_part
        else:
            buffer.writeln("E: Number out of range")
            tmp_account = prompt_account(prompt, buffer, accounts)
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
