from ledger import ledger
import curses

curses.wrapper(ledger.run)

