import copy

from .treegram import ShiftRegister, Treegram


class FGram(Treegram):
    def calculate_treegrams(self, root):
        self.recurse(root)

    def recurse(self, root):
        children = ShiftRegister(self.p)

        if root.children:
            for c in root.children:
                children.shift(c.label)
                self.append([root.label] + copy.deepcopy(children.register))
            for _ in range(self.p - 1):
                children.shift("*")
                self.append([root.label] + copy.deepcopy(children.register))
            for c in root.children:
                self.recurse(c)
