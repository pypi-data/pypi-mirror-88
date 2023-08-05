import copy

from .treegram import ShiftRegister, Treegram


class AngularL(Treegram):
    def calculate_treegrams(self, root):
        ancestors = ShiftRegister(self.p)
        self.recurse(root, ancestors)

    def recurse(self, root, ancestors, inner=False):
        ancestors.shift(root.label)
        siblings = ShiftRegister(self.q)

        if root.children:
            for c in root.children:
                siblings.shift(c.label)
                if not inner or ancestors.register[0] != "*":
                    self.append(ancestors.concatenate(siblings))

            for _ in range(self.q - 1):
                siblings.shift("*")
                if not inner or ancestors.register[0] != "*":
                    self.append(ancestors.concatenate(siblings))

            for i, c in enumerate(root.children):
                if i == 0:
                    self.recurse(c, copy.deepcopy(ancestors), inner)
                else:
                    self.recurse(c, ShiftRegister(self.p), True)
