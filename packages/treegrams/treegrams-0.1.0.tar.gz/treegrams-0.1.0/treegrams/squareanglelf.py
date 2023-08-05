from .treegram import Node, ShiftRegister, Treegram


class SquareAngleLF(Treegram):
    def calculate_treegrams(self, root):
        temp = Node("*")
        temp.addkid(root)
        root = temp
        self.recurse(root)

    def recurse(self, root):
        siblings = ShiftRegister(self.p)
        qs = None

        if root.children:
            qs = self.get_l_part(root.children[0])
        else:
            return

        for c in root.children:
            siblings.shift(c.label)
            self.append([root.label] + siblings.concatenate(qs))

        for _ in range(self.p - 1):
            siblings.shift("*")
            self.append([root.label] + siblings.concatenate(qs))

        for c in root.children:
            self.recurse(c)

    def get_l_part(self, root):
        ret = ShiftRegister(self.q)
        ret.shift(root.label)
        counter = 1
        while counter < self.q:
            counter += 1
            if root.children:
                root = root.children[0]
                ret.shift(root.label)
            else:
                ret.shift("*")
        return ret
