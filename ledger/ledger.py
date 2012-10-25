import argparse
from io import TextIOBase
import os
import sys
from ledger.account import Accounts
from ledger.actions import read_csv, read_ledger_accounts
from ledger.buffer import Buffer
from ledger.completer import Completer
import curses
import json


actions = {
    'parsecsv': read_csv
}

def setup_ncurses():
    lines = int(os.environ['LINES'])
    columns = int(os.environ['COLUMNS'])
    half_width = int(columns / 2)

    left_window = curses.newwin(lines, half_width)
    right_window = curses.newwin(lines, half_width, 0, half_width + 2)

    left_buffer = Buffer(left_window, lines, half_width)
    right_buffer = Buffer(right_window, lines)

    return left_buffer, right_buffer


def run(stdscr, args):
    curses.echo()

    left_buffer, right_buffer = setup_ncurses()

    input_filename = os.path.expanduser(args['input'])
    if args['action'] == 'parsecsv':
        accounts = Accounts(right_buffer)

        if args['ledger_file']:
            account_list = sorted(
                list(
                    read_ledger_accounts(
                        os.path.expanduser(args['ledger_file'])
                    )
                )
            )
            accounts.add_accounts(account_list, False)
            accounts.sort()
            accounts.print_accounts()

        entries = read_csv(input_filename)

        completer = Completer(left_buffer, accounts, entries)

        entries = completer.complete_entries()

        f = args['output']

        for entry in entries:
            f.write(entry.as_ledger_entry())
            f.write("\n\n")

    left_buffer.input_chr("Finished, press any key to continue")