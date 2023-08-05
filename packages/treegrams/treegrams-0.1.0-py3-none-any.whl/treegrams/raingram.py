from .treegram import ShiftRegister, Treegram


class RainGram(Treegram):
    def calculate_treegrams(self, root):
        self.recurse(root)

    def recurse(self, root):
        h = ShiftRegister(self.p)
        for c in root.children:
            h.shift(c.label)
            for s in c.parent.children:
                for v in self.get_possible_vs(s, self.q):
                    self.append(h.concatenate(v))

        for _ in range(self.p - 1):
            h.shift("*")
            for s in root.children:
                for v in self.get_possible_vs(s, self.q):
                    self.append(h.concatenate(v))

        for c in root.children:
            self.recurse(c)

    def get_possible_vs(self, node, maxlength):
        ret = []
        if maxlength == 1:
            tmp = ShiftRegister(1)
            tmp.shift(node.label)
            ret.append(tmp)
        elif maxlength > 1:
            if not node.children:
                tmp = ShiftRegister(maxlength)
                tmp.shift(node.label)
                for _ in range(maxlength - 1):
                    tmp.shift("*")
                ret.append(tmp)
            for child in node.children:
                for v in self.get_possible_vs(child, maxlength - 1):
                    tmp = ShiftRegister(maxlength)
                    tmp.shift(node.label)
                    for j in range(maxlength - 1):
                        tmp.shift(v.register[j])
                    ret.append(tmp)
        return ret
