import copy

from .treegram import ShiftRegister, Treegram


class HLine(Treegram):
    def calculate_treegrams(self, root):
        self.recurse(root)

    def recurse(self, root):
        siblings = ShiftRegister(self.p)
        if root.children:
            for c in root.children:
                siblings.shift(c.label)
                self.append(copy.deepcopy(siblings.register))
                self.recurse(c)
            for _ in range(self.p - 1):
                siblings.shift("*")
                self.append(copy.deepcopy(siblings.register))
