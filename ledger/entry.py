class Entry:
    def __init__(self):
        self.date = ""
        self.amount = ""
        self.description = ""
        self.account_from = ""
        self.account_to = ""

    def as_ledger_entry(self):
        ledger_entry = "{} * {}\n".format(self.date, self.description)

        ledger_entry += "\t{}{}{}\n".format(self.account_to, "\t" * 5, self.amount)
        ledger_entry += "\t{}".format(self.account_from)

        return ledger_entry

    def __str__(self):
        output = "Date: {self.date}\n" \
                 "Amount: {self.amount}\n" \
                 "Description: {self.description}\n"

        output += "Account from: {}\n".format(self.account_from)

        output += "Account to: {}\n".format(self.account_to)

        return output.format(self=self)