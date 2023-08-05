from sklearn.base import BaseEstimator, TransformerMixin
import logging
logger = logging.getLogger(__name__)

from . import get_tgram_by_name


class TreeGramExtractor(TransformerMixin, BaseEstimator):
    """
    input: one document = list of list of nltk.Tree objects
    output: one document = list of strings
    """

    def __init__(self, tgram='PQGram', p=2, q=3, r=None, join_symbol='_'):
        self.tgram = tgram
        self.p = p
        self.q = q
        self.r = r
        self.join_symbol = join_symbol

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        tree_class = get_tgram_by_name(self.tgram)
        total_result = []
        for document in x:
            document_ret = []
            for sentence in document:
                if type(sentence) == list:
                    if len(sentence) > 1:
                        raise Exception(
                            f'More than one sentence, some info seems to be '
                            f'skipped: {document}'
                        )
                    elif len(sentence) == 1:
                        sentence = sentence[0]
                    else:
                        continue
                try:
                    grams = tree_class(sentence, self.p, self.q, self.r)
                    document_ret += [self.join_symbol.join(x) for x in grams]
                except ValueError as e:
                    logger.error('parsing failed for sentence: %s', sentence)
                    logger.error(e)
            total_result.append(document_ret)
        if not total_result:
            raise ValueError(f'could not parse anything from input: {x}')
        return total_result
