import argparse
import os
from ledger.actions import read_csv, complete_entries
from ledger.buffer import Buffer
import curses

parser = argparse.ArgumentParser(description="Adds entries to a ledger file")
parser.add_argument('action')
parser.add_argument('input')

actions = {
    'parsecsv': read_csv
}

def run(stdscr):
    lines = int(os.environ['LINES'])
    curses.echo()
    buffer = Buffer(stdscr, lines)
    args = parser.parse_args()
    input_filename = os.path.expanduser(args.input)
    if args.action == 'parsecsv':
        entries = read_csv(input_filename, os.path.expanduser("~/Documents/boekhouding.dat"))
        entries = complete_entries(buffer, entries)
        stdscr.refresh()
        stdscr.getch()


