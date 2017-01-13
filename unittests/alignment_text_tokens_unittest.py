import unittest
from hamcrest import *

from prioritised_xml_collation.EditGraphAligner import EditGraphAligner
from prioritised_xml_collation.coordination import align_tokens_and_return_superwitness
from prioritised_xml_collation.tokenizer import Tokenizer, TextToken
from prioritised_xml_collation.replacement_scorer import ReplacementScorer


class SuperwitnessText(unittest.TestCase):
    @unittest.skip("Unittest fails if near_matching on punctuation is turned off.")
    def test_superwitness_tokens_near_matching_on_punctuation(self):
        witA = open("../input_xml/witA-s021-simple.xml")
        witB = open("../input_xml/witB-s021-simple.xml")
        tokenizer = Tokenizer()
        tokens_a = tokenizer.convert_xml_file_into_tokens(witA)
        tokens_b = tokenizer.convert_xml_file_into_tokens(witB)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        list_superwitness_string = [str(token) for token in superwitness]
        print(list_superwitness_string)
        expected = ['Hoe', 'zoet', 'moet', 'nochtans', 'zijn', 'dit', 'werven', 'om', 'trachten', 'naar', 'een',
                    'vrouw', '-,', '+!', '-de', '-ongewisheid', '+Die', '+dagen', '+van', '+nerveuze', '+verwachting',
                    'vóór', 'de', 'liefelijke', 'toestemming', '-!', '+.']
        self.assertEqual(expected, list_superwitness_string)

    def test_superwitness_tokens(self):
        witA = open("../input_xml/witA-s021-simple.xml")
        witB = open("../input_xml/witB-s021-simple.xml")
        tokenizer = Tokenizer()
        tokens_a = tokenizer.convert_xml_file_into_tokens(witA)
        tokens_b = tokenizer.convert_xml_file_into_tokens(witB)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        list_superwitness_string = [str(segment) for segment in superwitness]
        print(list_superwitness_string)
        expected = ['text, body, div, p, s, Hoe, zoet, moet, nochtans, zijn, dit', "['-lb', '-/lb']",
                    'del, werven, om, /del, add, trachten, naar, /add, een', "['+lb', '+/lb']", 'vrouw',
                    "['-,', '-de', '-ongewisheid']->['+!', '+/s', '+s', '+Die', '+dagen', '+van', '+nerveuze', '+verwachting']",
                    'vóór, de', "['+lb', '+/lb']", 'liefelijke, toestemming', "['-!']->['+.']",
                    '/s, /p, /div, /body, /text']
        self.assertEqual(expected, list_superwitness_string)

    @unittest.skip("Unittest fails because alignment code is not yet performing correctly")
    def test_superwitness_segmentation(self):
        witA = open("../input_xml/witA-s021-simple.xml")
        witB = open("../input_xml/witB-s021-simple.xml")
        tokenizer = Tokenizer()
        tokens_a = tokenizer.convert_xml_file_into_tokens(witA)
        tokens_b = tokenizer.convert_xml_file_into_tokens(witB)
        # get results of segmented superwitness from method below
        segmented_superwitness = self.refine_segments_of_superwitness(tokens_a, tokens_b)
        # expected output is a tuple of two values:
        # a string representation of the edit operation
        # and a string representation of the token concent
        expected = [("aligned", "[text, body, div, p, s, Hoe, zoet, moet, nochtans, zijn, dit]"),
                    ("-", "[lb, /lb]"), ("aligned", "[del, werven, om, /del, add, trachten, naar, /add, een]"),
                    ("+", "[lb, /lb]"), ("aligned", "[vrouw]"),
                    ("replaced", "[,, de, ongewisheid] -> [!, Die, dagen, van, nerveuze, verwachting]"),
                    ("aligned", "[vóór, de]"), ("+", "[lb, /lb]"), ("aligned", "[liefelijke, toestemming]"),
                    ("replaced", "[!] -> [.]"), ("aligned", "[/s, /p, /div, /body, /text]")]
        self.assertEqual(expected, segmented_superwitness)

    def test_match_punctuation(self):
        token_A = TextToken(",")
        token_B = TextToken("!")
        score_punctuation = ReplacementScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        self.assertEqual(0, punctuation_tokens)

    def test_no_match_punctuation(self):
        token_A = TextToken("Hoe")
        token_B = TextToken("!")
        score_punctuation = ReplacementScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        assert_that(punctuation_tokens, is_(-1))
        # self.assertEqual(-1, punctuation_tokens)

    def test_no_match_either_punctuation(self):
        token_A = TextToken(",")
        token_B = TextToken("dit")
        score_punctuation = ReplacementScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        expected = -1
        self.assertEqual(expected, punctuation_tokens)

    def test_another_match_punctuation(self):
        token_A = TextToken("...")
        token_B = TextToken(",")
        score_punctuation = ReplacementScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        expected = 0
        self.assertEqual(expected, punctuation_tokens)

    def refine_segments_of_superwitness(self, tokens_a, tokens_b):
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        segmented_superwitness = []
        # segment is an pointer to the object Segment and has therefore the fields, methods of the object Segment
        for segment in superwitness:
            print(segment)
            tokens_witness_a, tokens_witness_b = segment.tokens
            if not segment.aligned:
                if segment.replacement:
                    segmented_superwitness.append(("replaced", str(tokens_witness_a) + " -> " + str(tokens_witness_b)))
                elif segment.addition:
                    segmented_superwitness.append(("+", str(tokens_witness_b)))
                else:
                    # segment is omission
                    segmented_superwitness.append(("-", str(tokens_witness_a)))
            # else it is aligned:
            else:
                segmented_superwitness.append(("aligned", str(tokens_witness_a)))
        return segmented_superwitness
