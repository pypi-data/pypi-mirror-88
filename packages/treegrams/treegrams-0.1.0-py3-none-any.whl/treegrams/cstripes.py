import copy

from .treegram import ShiftRegister, Treegram


class CStripes(Treegram):
    def calculate_treegrams(self, root):
        ancestors = ShiftRegister(self.p)
        self.recurse(root, ancestors)

    def recurse(self, root, ancestors, inner=False):

        ancestors.shift(root.label)
        if not inner or ancestors.register[0] != "*":
            self.append(copy.deepcopy(ancestors.register))

        if root.children:
            for i, c in enumerate(root.children):
                if len(root.children) % 2 == 1 \
                        and i == len(root.children) // 2:
                    self.recurse(c, copy.deepcopy(ancestors), inner=inner)
                else:
                    self.recurse(c, ShiftRegister(self.p), inner=True)

        if not root.children or len(root.children) % 2 == 0:
            for _ in range(self.p - 1):
                ancestors.shift("*")
                if not inner or ancestors.register[0] != "*":
                    self.append(copy.deepcopy(ancestors.register))
