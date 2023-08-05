# from .tgram import TGram
from .angularl import AngularL
from .angularr import AngularR
from .cstripes import CStripes
from .fgram import FGram
from .hline import HLine
from .lstripes import LStripes
from .pqgram import PQGram
from .raingram import RainGram
from .raingraml import RainGramL
from .raingramr import RainGramR
from .rstripes import RStripes
from .squareanglel import SquareAngleL
from .squareanglelf import SquareAngleLF
from .squareangler import SquareAngleR
from .squareanglerf import SquareAngleRF
from .stripes import Stripes
from .threestripes import ThreeStripes
from .vgram import VGram

all_grams = {
    1: {
        "CStripes": CStripes,
        "FGram": FGram,
        "HLine": HLine,
        "Stripes": Stripes,
        "LStripes": LStripes,
        "RStripes": RStripes,
    },
    2: {
        "PQGram": PQGram,
        "AngularL": AngularL,
        "AngularR": AngularR,
        "VGram": VGram,
        "SquareAngleL": SquareAngleL,
        "SquareAngleR": SquareAngleR,
        "SquareAngleLF": SquareAngleLF,
        "SquareAngleRF": SquareAngleRF,
        "RainGram": RainGram,
        "RainGramL": RainGramL,
        "RainGramR": RainGramR,
    },
    3: {"ThreeStripes": ThreeStripes},
}


def get_all_treegram_names():
    for v in all_grams.values():
        for tg_name in v.keys():
            yield tg_name


def get_all_treegram_types():
    for v in all_grams.values():
        for tg_type in v.values():
            yield tg_type


def get_all_treegrams():
    for k, v in all_grams.items():
        for (sub_k, sub_v) in v.items():
            yield sub_k, sub_v


def get_tgram_by_name(name):
    for v in all_grams.values():
        if name in v:
            return v[name]
    raise Exception("no such tree type: %s" % name)


def get_all_variant_names_for_all_types():
    data = get_all_variants_for_all_types()
    return [x[0] for x in data]


def get_all_variants_for_all_types():
    ret = []

    for tg_name, tg_type in get_all_treegrams():
        if get_variable_count_for_type(tg_name) == 1:
            for p in range(2, 5):
                run_name = "%s@P=%d" % (tg_name, p)
                ret.append((run_name, tg_type, p))
        if get_variable_count_for_type(tg_name) == 2:
            for p in range(2, 5):
                for q in range(2, 5):
                    run_name = "%s@P=%dQ=%d" % (tg_name, p, q)
                    ret.append((run_name, tg_type, p, q))
        if get_variable_count_for_type(tg_name) == 3:
            for p in range(2, 4):
                for q in range(2, 4):
                    for r in range(2, 4):
                        run_name = "%s@P=%dQ=%dR=%d" % (tg_name, p, q, r)
                        ret.append((run_name, tg_type, p, q, r))
    return ret


def get_variable_count_for_type(tg_name):
    for k, v in all_grams.items():
        if tg_name in v:
            return k
    raise ValueError("no such tree type: %s" % tg_name)
