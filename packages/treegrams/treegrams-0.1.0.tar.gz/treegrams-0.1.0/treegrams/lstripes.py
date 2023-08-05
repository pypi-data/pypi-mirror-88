import copy

from .treegram import ShiftRegister, Treegram


class LStripes(Treegram):
    def calculate_treegrams(self, root):
        ancestors = ShiftRegister(self.p)
        self.recurse(root, ancestors)

    def recurse(self, root, ancestors, inner=False):

        ancestors.shift(root.label)
        if not inner or ancestors.register[0] != "*":
            self.append(copy.deepcopy(ancestors.register))

        if root.children:
            for i, c in enumerate(root.children):
                if i == 0:
                    self.recurse(c, copy.deepcopy(ancestors), inner=inner)
                else:
                    self.recurse(c, ShiftRegister(self.p), inner=True)

        else:
            for _ in range(self.p - 1):
                ancestors.shift("*")
                if not inner or ancestors.register[0] != "*":
                    self.append(copy.deepcopy(ancestors.register))
