import argparse
import sys
from ledger import ledger
import curses

parser = argparse.ArgumentParser(description="Adds entries to a ledger file")
parser.add_argument('action')
parser.add_argument('input')
parser.add_argument('--ledger-file', dest='ledger_file', nargs=1)

args = parser.parse_args()

try:
    curses.wrapper(ledger.run, args)
except KeyboardInterrupt:
    pass
