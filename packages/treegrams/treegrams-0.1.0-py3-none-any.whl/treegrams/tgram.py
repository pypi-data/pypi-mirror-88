from .treegram import ShiftRegister, Treegram


class TGram(Treegram):
    def calculate_treegrams(self, root):
        ancestors = ShiftRegister(self.p)
        self.recurse(root, ancestors)

    def recurse(self, root, ancestors):
        """
        Recursively builds the PQ-Gram profile of the given subtree. This
        method should not be called directly and is called from __init__.
        """
        ancestors.shift(root.label)

        for _ in range(self.p - 1):
            ancestors.shift("*")

    def get_c_part(self, root):
        ret = ShiftRegister(self.q)
        ret.shift(root.label)
        while root.children and len(root.children) % 2 == 1:
            root = root.children[len(root.children) // 2]
            ret.shift(root.label)
        while ret.register[0] == "*":
            ret.shift("*")
        return ret
