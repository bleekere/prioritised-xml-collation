from prioritised_xml_collation.EditGraphAligner import EditGraphAligner


def align_tokens_and_return_superwitness(tokens1, tokens2):
    # align sequences of tokens. Results in segments.
    aligner = EditGraphAligner()
    aligner.align(tokens1, tokens2)
    superwitness = aligner.superwitness
    return superwitness
