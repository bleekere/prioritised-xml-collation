from prioritised_xml_collation.EditGraphAligner import EditGraphAligner

# NB differentiate between ContentScorer and TypeScorer: how?
from prioritised_xml_collation.content_scorer import ContentScorer
from prioritised_xml_collation.type_scorer import TypeScorer


def align_tokens_and_return_superwitness(tokens1, tokens2):
    # align sequences of tokens. Results in segments.
    content_scorer = ContentScorer()
    aligner = EditGraphAligner(content_scorer)
    aligner.align(tokens1, tokens2)
    superwitness = aligner.superwitness
    return superwitness

def align_tokens_on_type_and_return_superwitness(tokens1, tokens2):
    # align sequence of tokens ON TYPE. Results in segments.
    # get TypeScorer: how?
    type_scorer = TypeScorer()
    aligner = EditGraphAligner(type_scorer)
    aligner.align(tokens1, tokens2)
    second_superwitness = aligner.superwitness
    return second_superwitness