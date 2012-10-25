from decimal import Decimal
from ledger.entry import Entry

class Completer(object):
    def __init__(self, buffer, accounts, entries):
        self.buffer = buffer
        self.accounts = accounts
        self.entries = entries
        self.account_from = ""
        self.action = ""
        self.index = 0
        self.max = 0

    def save_entry(self, entry):
        if not entry.account_from or not entry.account_to:
            confirm = self.buffer.input_chr("Account information not complete. Still want to edit? (Y/n) ")
            if confirm != "n":
                self.action = "a"
            else:
                self.index += 1
        else:
            self.index += 1

    def complete_accounts(self, entry):
        if entry.amount > 0:
            entry.account_to = self.account_from
            entry.account_from = self.prompt_account("Account from (income): ")
        else:
            entry.amount = abs(entry.amount)
            entry.account_to = self.prompt_account("Account to (expense): ")
            entry.account_from = self.account_from


    def create_new_entry(self, amount, date):
        new_entry = Entry()
        new_entry.amount = Decimal(amount)
        new_entry.date = date
        return new_entry

    def split_statements(self, entry):
        nr_of_statements = self.prompt_number_of_statements()
        amount_left = entry.amount

        del(self.entries[self.index])

        for i in range(0, nr_of_statements - 1):
            amount = self.buffer.input("Amount of statement {} ({} left): ".format(i + 1, amount_left))
            new_entry = self.create_new_entry(amount, entry.date)
            amount_left -= new_entry.amount
            self.entries.insert(self.index + i, new_entry)
            self.buffer.writeln("Inserting item at index {}".format(self.index + i))

        new_index = self.index + nr_of_statements - 1
        self.buffer.input_chr("Amount of statement {}: {}".format(nr_of_statements, amount_left))
        self.entries.insert(new_index, self.create_new_entry(amount_left, entry.date))
        self.max += nr_of_statements - 1

    def edit_description(self, entry):
        entry.description = self.buffer.input("Description: ")

    def print_entry(self, entry):
        self.buffer.scroll_top()
        self.buffer.writeln("Entry {} of {}\n".format(self.index + 1, self.max))
        self.buffer.writeln(str(entry))

    def complete_entries(self):

        self.account_from = self.prompt_account("Default account from: ")

        self.max = len(self.entries)
        while self.index < self.max:
            entry = self.entries[self.index]

            self.print_entry(entry)

            action = self.buffer.input_chr("Action ((E)dit description, Set (A)ccounts, S(P)lit, (S)ave) > ")

            actions = {
                "s": self.save_entry,
                "e": self.edit_description,
                "a": self.complete_accounts,
                "p": self.split_statements
            }

            if action in actions:
                actions[action](entry)

            self.buffer.writeln()

        return self.entries

    def prompt_number_of_statements(self):
        try:
            return int(self.buffer.input("How many statements? "))
        except ValueError:
            self.buffer.writeln("You're supposed to give a number")
            return self.prompt_number_of_statements()


    def prompt_account(self, prompt):
        account_response = self.buffer.input(prompt)

        if account_response.isdigit():
            nr = int(account_response)
            if nr < len(self.accounts):
                selected_account = self.accounts[int(account_response)]
                self.buffer.write(prompt + selected_account + ":")
                account_part = self.buffer.input()

                if account_part != "":
                    selected_account += ":" + account_part
            else:
                self.buffer.writeln("E: Number out of range")
                selected_account = self.prompt_account(prompt)
        elif not account_response == "":
            selected_account = account_response
        else:
            selected_account = self.prompt_account(prompt)

        self.accounts.add_account(selected_account)
        return selected_account