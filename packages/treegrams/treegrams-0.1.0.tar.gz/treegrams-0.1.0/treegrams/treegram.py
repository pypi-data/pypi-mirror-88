from abc import ABC, abstractmethod

from nltk import Tree


class Treegram(ABC):
    def __init__(self, root, p=2, q=3, r=3):
        super(Treegram, self).__init__()

        if p == 0:
            raise ValueError("p must be greater than 0")

        if type(root) == str:
            root = Tree.fromstring(root)
        if type(root) == Tree:
            gram_tree = self.nltk_to_treegram(root)
        else:
            gram_tree = root
        self.list = list()
        self.p = p
        self.q = q
        self.r = r
        self.calculate_treegrams(gram_tree)

    def nltk_to_treegram(self, tree):
        if hasattr(tree, "_label"):
            node = Node(tree._label)
            for t in tree:
                child = self.nltk_to_treegram(t)
                if child:
                    node.addkid(child)
            return node
        return None

    @abstractmethod
    def calculate_treegrams(self, root):
        pass

    def out(self):
        return ["_".join(x) for x in self.list]

    def sort(self):
        self.list.sort(key=lambda x: "".join(x))

    def append(self, value):
        self.list.append(value)

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return str(self.list)

    def __str__(self):
        return str(["_".join(x) for x in self.list])

    def __getitem__(self, key):
        return self.list[key]

    def __iter__(self):
        for x in self.list:
            yield x


class ShiftRegister(object):
    def __init__(self, size):
        self.register = list()
        for _ in range(size):
            self.register.append("*")

    def concatenate(self, reg):
        temp = list(self.register)
        temp.extend(reg.register)
        return temp

    def shift(self, el):
        self.register.pop(0)
        self.register.append(el)

    def __str__(self):
        return str(self.register)

    def __repr__(self):
        return str(self.register)


class Node(object):
    def __init__(self, label):
        self.parent = None
        self.label = label
        self.children = list()

    def addkid(self, node, before=False):
        node.parent = self
        if before:
            self.children.insert(0, node)
        else:
            self.children.append(node)
        return self

    def get_siblings(self):
        if self.parent is None:
            return []
        return [x for x in self.parent.children if x is not self]

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label
