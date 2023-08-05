from .cstripes import CStripes
from .lstripes import LStripes
from .rstripes import RStripes
from .treegram import Treegram


class ThreeStripes(Treegram):
    def calculate_treegrams(self, root):
        _l = LStripes(root, self.p).list
        _r = RStripes(root, self.q).list
        _c = CStripes(root, self.r).list
        ret = _l + _r + _c
        ret.sort(key=lambda x: "".join(x))
        self.list = ret
