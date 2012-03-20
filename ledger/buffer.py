class Buffer(object):

    def __init__(self, window, lines, columns=0):
        self.window = window
        self.lines = lines
        self.buffer = [""]
        self.columns = columns

    def write(self, text):
        lines = text.split("\n")
        self.buffer[-1] += lines[0]
        self.buffer.extend(lines[1:])

        for i in range(len(self.buffer) - len(lines) - 1, len(self.buffer)):
            self._fix_long_line(i)

        self.refresh()

    def writeln(self, text = ""):
        self.write(text + "\n")

    def input(self, text = ""):
        return self._input(text, lambda: self.window.getstr().decode('utf-8'))

    def input_chr(self, text = ""):
        return self._input(text, lambda: chr(self.window.getch()))

    def _input(self, text, get_input):
        self.write(text)
        input = get_input()
        self.writeln(input)
        return input

    def scroll_top(self):
        #TODO: Scroll instead of clear
        self.clear()

    def clear(self):
        self.buffer = [""]
        self.refresh()

    def refresh(self):
        self.window.clear()
        for nr, line in enumerate(self.buffer[-self.lines:]):
            self.window.addstr(nr, 0, line)
        self.window.refresh()

    def _fix_long_line(self, line):
        if not self.columns: return

        if len(self.buffer[line]) > self.columns:
            part = self.buffer[line]
            parts = []
            while len(part):
                parts.append(part[:self.columns])
                part = part[self.columns:]

            parts.reverse()
            del(self.buffer[line])
            for part in parts:
                self.buffer.insert(line, part)
