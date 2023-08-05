import copy

from .treegram import ShiftRegister, Treegram


class Stripes(Treegram):
    def calculate_treegrams(self, root):
        ancestors = ShiftRegister(self.p)
        self.recurse(root, ancestors)

    def recurse(self, root, ancestors):

        ancestors.shift(root.label)
        self.append(copy.deepcopy(ancestors.register))

        if root.children:
            for c in root.children:
                self.recurse(c, copy.deepcopy(ancestors))
        else:
            for _ in range(self.p - 1):
                ancestors.shift("*")
                self.append(copy.deepcopy(ancestors.register))
