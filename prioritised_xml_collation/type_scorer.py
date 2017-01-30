from Levenshtein import ratio
from prioritised_xml_collation.AbstractClassScorer import Scorer
from prioritised_xml_collation.tokenizer import ElementToken
import re


class TypeScorer(Scorer):
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

    # TODO match now defined as tokens are both punctuation or both markup; we want to test also on type=text
