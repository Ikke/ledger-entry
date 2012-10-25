#!/usr/bin/env python
import argparse
import os
import sys
from ledger import ledger
import curses

parser = argparse.ArgumentParser(description="Adds entries to a ledger file")
parser.add_argument('action', help="Currently only 'parsecsv'")
parser.add_argument('input', help="The file to read the statements from, currently only ABN AMRO tsv's are supported")
parser.add_argument(
    '--ledger-file',
    dest='ledger_file',
    nargs=1,
    help="The ledger file to get accounts from"
)
parser.add_argument(
    '--output',
    dest='output',
    nargs=1,
    help="The file to write the output to. Use - for stdout"
)

args = parser.parse_args()

params = {}

if args.ledger_file:
    params['ledger_file'] = args.ledger_file[0]
elif os.environ['LEDGER_FILE']:
    params['ledger_file'] = os.environ['LEDGER_FILE']

if args.output:
    params['output'] = open(args.output[0], 'a')
elif params.get('ledger_file'):
    params['output'] = open(params['ledger_file'], 'a')
else:
    params['output'] = sys.stdout

params['action'] = args.action
params['input'] = args.input

try:
    curses.wrapper(ledger.run, params)
except KeyboardInterrupt:
    pass
