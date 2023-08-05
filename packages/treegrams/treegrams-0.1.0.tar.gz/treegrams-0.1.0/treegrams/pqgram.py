import copy

from .treegram import ShiftRegister, Treegram


class PQGram(Treegram):
    def calculate_treegrams(self, root):
        ancestors = ShiftRegister(self.p)
        self.recurse(root, ancestors)

    def recurse(self, root, ancestors):
        ancestors.shift(root.label)
        siblings = ShiftRegister(self.q)

        if len(root.children) == 0 and siblings.register[0] != "*":
            tmp = ancestors.concatenate(siblings)
            # self.append(tmp)
        if root.children:
            for child in root.children:
                siblings.shift(child.label)
                tmp = ancestors.concatenate(siblings)
                self.append(tmp)
                self.recurse(child, copy.deepcopy(ancestors))
            for _ in range(self.q - 1):
                siblings.shift("*")
                tmp = ancestors.concatenate(siblings)
                self.append(tmp)
