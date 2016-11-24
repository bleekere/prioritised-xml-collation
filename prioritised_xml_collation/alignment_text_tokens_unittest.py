import unittest

from prioritised_xml_collation.EditGraphAligner import EditGraphAligner
from prioritised_xml_collation.tokenizer_unittest import convert_xml_file_into_tokens


def align_tokens_and_return_superwitness(tokens1, tokens2):
    # align sequences of tokens. Results in segments.
    aligner = EditGraphAligner()
    aligner.align(tokens1, tokens2)
    superwitness = aligner.superwitness
    return superwitness


class SuperwitnessText(unittest.TestCase):
    @unittest.skip("Unittest fails if near_matching on punctuation is turned off.")
    def test_superwitness_tokens_near_matching_on_punctuation(self):
        witA = open("input_xml/witA-s021-simple.xml")
        witB = open("input_xml/witB-s021-simple.xml")
        tokens_a = convert_xml_file_into_tokens(witA)
        tokens_b = convert_xml_file_into_tokens(witB)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        list_superwitness_string = [str(token) for token in superwitness]
        print(list_superwitness_string)
        expected = ['Hoe', 'zoet', 'moet', 'nochtans', 'zijn', 'dit', 'werven', 'om', 'trachten', 'naar', 'een', 'vrouw', '-,', '+!', '-de', '-ongewisheid', '+Die', '+dagen', '+van', '+nerveuze', '+verwachting', 'vóór', 'de', 'liefelijke', 'toestemming', '-!', '+.']
        self.assertEqual(expected, list_superwitness_string)

    def test_superwitness_tokens(self):
        witA = open("input_xml/witA-s021-simple.xml")
        witB = open("input_xml/witB-s021-simple.xml")
        tokens_a = convert_xml_file_into_tokens(witA)
        tokens_b = convert_xml_file_into_tokens(witB)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        list_superwitness_string = [str(token) for token in superwitness]
        print(list_superwitness_string)
        expected = ['Hoe', 'zoet', 'moet', 'nochtans', 'zijn', 'dit', 'werven', 'om', 'trachten', 'naar', 'een',
                    'vrouw', '-,', '-de', '-ongewisheid', '+!', '+Die', '+dagen', '+van', '+nerveuze', '+verwachting',
                    'vóór', 'de', 'liefelijke', 'toestemming', '-!', '+.']
        self.assertEqual(expected, list_superwitness_string)

