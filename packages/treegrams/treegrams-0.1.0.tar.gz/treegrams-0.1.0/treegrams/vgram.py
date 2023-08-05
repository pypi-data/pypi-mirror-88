from .treegram import ShiftRegister, Treegram


class VGram(Treegram):
    def calculate_treegrams(self, root):
        self.recurse(root)

    def recurse(self, root):

        lefts = self.get_l_part(root, self.p)
        rights = self.get_r_part(root, self.q)

        self.append(lefts.concatenate(rights))
        for c in root.children:
            self.recurse(c)

    def get_r_part(self, root, maxlength):
        ret = ShiftRegister(maxlength)
        ret.shift(root.label)
        while maxlength > 0:
            if root.children:
                root = root.children[len(root.children) - 1]
                ret.shift(root.label)
            else:
                ret.shift("*")
            maxlength -= 1
        return ret

    def get_l_part(self, root, maxlength):
        ret = ShiftRegister(maxlength)
        ret.shift(root.label)
        while maxlength > 1:
            if root.children:
                root = root.children[0]
                ret.shift(root.label)
            else:
                ret.shift("*")
            maxlength -= 1
        return ret
