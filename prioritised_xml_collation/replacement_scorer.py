from Levenshtein import ratio
from prioritised_xml_collation.abstract_scorer import Scorer
from prioritised_xml_collation.tokenizer import ElementToken
import re


class ReplacementScorer(Scorer):
    def __init__(self):
        pass

    def match(self, token_a, token_b):
        # Note that at this point the tokens are not a conventional match (on textual content) anyway
        # content of token is string
        match = (re.match('\W', token_a.content) and re.match('\W', token_b.content)) or (
        isinstance(token_a, ElementToken) and isinstance(token_b, ElementToken))
        if match:
            return 0
        else:
            return -1
