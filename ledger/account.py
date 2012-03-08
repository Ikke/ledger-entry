class Accounts(object):
    def __init__(self, buffer):
        self.buffer = buffer
        self.accounts = []

    def add_account(self, account, print = True):
        if account and account not in self.accounts:
            self.accounts.append(account)
            self.add_account(":".join(account.split(":")[:-1]))
            if print:
                self.print_accounts()

    def add_accounts(self, accounts, print = True):
        for account in accounts:
            self.add_account(account, False)
        if print:
            self.print_accounts()

    def __getitem__(self, item):
        return self.accounts[item]

    def print_accounts(self):
        self.buffer.clear()
        for index, account in enumerate(self.accounts):
            self.buffer.writeln("{:02}: {}".format(index, account))

    def sort(self):
        self.accounts = sorted(self.accounts)