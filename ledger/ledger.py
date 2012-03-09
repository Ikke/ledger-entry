import argparse
from io import TextIOBase
import os
import sys
from ledger.account import Accounts
from ledger.actions import read_csv, complete_entries, read_ledger_accounts
from ledger.buffer import Buffer
import curses
import json


actions = {
    'parsecsv': read_csv
}

def run(stdscr, args):
    curses.echo()

    lines = int(os.environ['LINES'])
    columns = int(os.environ['COLUMNS'])

    half_width = int(columns / 2)

    left_window = curses.newwin(lines, half_width)
    left_buffer = Buffer(left_window, lines)

    right_window = curses.newwin(lines, half_width, 0, half_width + 2)
    right_buffer = Buffer(right_window, lines)

    input_filename = os.path.expanduser(args.input)
    if args.action == 'parsecsv':
        accounts = Accounts(right_buffer)

        if args.ledger_file:
            account_list = sorted(list(read_ledger_accounts(os.path.expanduser(args.ledger_file[0]))))
            accounts.add_accounts(account_list, False)
            accounts.sort()
            accounts.print_accounts()

        entries = read_csv(input_filename)
        entries = complete_entries(entries, accounts, left_buffer)

        f = open("test.dat", 'w')
        for entry in entries:
            f.write(entry.as_ledger_entry())
            f.write("\n\n")

    left_buffer.input_chr("Finished, press any key to continue")