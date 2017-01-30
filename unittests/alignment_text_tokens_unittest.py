import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.hasmethod import hasmethod

from prioritised_xml_collation.EditGraphAligner import EditGraphAligner
from prioritised_xml_collation.coordination import align_tokens_and_return_superwitness, \
    align_tokens_on_type_and_return_superwitness
from prioritised_xml_collation.tokenizer import Tokenizer, TextToken, ElementToken, Token
from prioritised_xml_collation.type_scorer import TypeScorer
from prioritised_xml_collation.EditGraphAligner import Node
from prioritised_xml_collation.custom_matchers import token_content


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

    @unittest.skip(
        "Unittest fails because alignment code is not yet performing as desired where it comes to the nested <s>")
    def test_superwitness_segmentation(self):
        self.maxDiff = None
        witA = open("../input_xml/witA-s021-simple.xml")
        witB = open("../input_xml/witB-s021-simple.xml")
        tokenizer = Tokenizer()
        tokens_a = tokenizer.convert_xml_file_into_tokens(witA)
        tokens_b = tokenizer.convert_xml_file_into_tokens(witB)
        # get results of segmented superwitness from method below
        segmented_superwitness = self.define_segments_of_superwitness(tokens_a, tokens_b)
        # expected output is a tuple of two values:
        # a string representation of the edit operation
        # and a string representation of the token concent
        expected = [("aligned", "[text, body, div, p, s, Hoe, zoet, moet, nochtans, zijn, dit]"),
                    ("-", "[lb, /lb]"), ("aligned", "[del, werven, om, /del, add, trachten, naar, /add, een]"),
                    ("+", "[lb, /lb]"), ("aligned", "[vrouw]"), ("replaced", "[,] -> [!]"), ("+", "[s, /s]"),
                    ("replaced", "[de, ongewisheid] -> [Die, dagen, van, nerveuze, verwachting]"),
                    ("aligned", "[vóór, de]"), ("+", "[lb, /lb]"), ("aligned", "[liefelijke, toestemming]"),
                    ("replaced", "[!] -> [.]"), ("aligned", "[/s, /p, /div, /body, /text]")]
        self.assertEqual(expected, segmented_superwitness)

    def test_match_punctuation(self):
        token_A = TextToken(",")
        token_B = TextToken("!")
        score_punctuation = TypeScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        self.assertEqual(0, punctuation_tokens)

    def test_no_match_punctuation(self):
        token_A = TextToken("Hoe")
        token_B = TextToken("!")
        score_punctuation = TypeScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        assert_that(punctuation_tokens, is_(-1))
        # self.assertEqual(-1, punctuation_tokens)

    def test_no_match_either_punctuation(self):
        token_A = TextToken(",")
        token_B = TextToken("vrouw")
        score_punctuation = TypeScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        self.assertEqual(-1, punctuation_tokens)

    def test_another_match_punctuation(self):
        token_A = TextToken("...")
        token_B = TextToken(",")
        score_punctuation = TypeScorer()
        punctuation_tokens = score_punctuation.match(token_A, token_B)
        self.assertEqual(0, punctuation_tokens)

    def test_punctuation_and_markup_match1(self):
        token_A = ElementToken("div")
        token_B = ElementToken("p")
        score_punctuation_and_markup = TypeScorer()
        punct_and_markup_tokens = score_punctuation_and_markup.match(token_A, token_B)
        assert_that(punct_and_markup_tokens, is_(0))

    def test_punctuation_and_markup_match2(self):
        token_A = TextToken("!")
        token_B = ElementToken("p")
        score_punctuation_and_markup = TypeScorer()
        punct_and_markup_tokens = score_punctuation_and_markup.match(token_A, token_B)
        assert_that(punct_and_markup_tokens, is_(-1))

    def test_punctuation_and_markup_match3(self):
        token_A = ElementToken("div")
        token_B = TextToken("Hoe")
        score_punctuation_and_markup = TypeScorer()
        punct_and_markup_tokens = score_punctuation_and_markup.match(token_A, token_B)
        assert_that(punct_and_markup_tokens, is_(-1))

    def test_punctuation_and_markup_match4(self):
        token_A = TextToken("zijn")
        token_B = TextToken("nerveuze")
        score_punctuation_and_markup = TypeScorer()
        punct_and_markup_tokens = score_punctuation_and_markup.match(token_A, token_B)
        assert_that(punct_and_markup_tokens, is_(0))

    def test_second_alignment(self):
        self.maxDiff = None
        witness_a = open("../input_xml/witA-replacement-alignment.xml")
        witness_b = open("../input_xml/witB-replacement-alignment.xml")
        # tokenize witnesses
        tokenizer = Tokenizer()
        tokens_a = tokenizer.convert_xml_file_into_tokens(witness_a)
        tokens_b = tokenizer.convert_xml_file_into_tokens(witness_b)
        # tokens are no textual match so we need type_scorer
        segmented_second_superwitness = self.define_segments_of_superwitness_on_type(tokens_a, tokens_b)
        print(segmented_second_superwitness)
        expected = [('aligned', '[text, s]', '[text, s]'), ('aligned', '[,]', '[?]'), ('-', '[de, ongewisheid]'), ('-', '[!]'),
                    ('aligned', '[/s]', '[/s, p]'), ('+', '[Die, dagen, van, nerveuze, verwachting]'), ('+', '[.]'),
                    ('aligned', '[/text]', '[/p, /text]')]
        assert_that(expected, segmented_second_superwitness)

    # def test_combined_alignment(self):
    #     self.maxDiff = None
    #     witness_a = open("../input_xml/witA-s021-2nd-alignment.xml")
    #     witness_b = open("../input_xml/witB-s021-2nd-alignment.xml")
    #     tokenizer = Tokenizer()
    #     tokens_a = tokenizer.convert_xml_file_into_tokens(witness_a)
    #     tokens_b = tokenizer.convert_xml_file_into_tokens(witness_b)
    #     self.two_step_alignment(tokens_a, tokens_b)
    #     self.fail(msg="Expected failure")

    def test_custom_matcher_token(self):
        actual_token = Token("text") # Token has one property "content"
        assert_that(actual_token, is_(token_content("text")))


    def define_segments_of_superwitness(self, tokens_a, tokens_b):
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


    def define_segments_of_superwitness_on_type(self, tokens_a, tokens_b):
        second_superwitness = align_tokens_on_type_and_return_superwitness(tokens_a, tokens_b)
        aligned_second_superwitness = []
        for segment in second_superwitness:
            tokens_witness_a, tokens_witness_b = segment.tokens
            # aligned on type match, not on content match
            if not segment.aligned:
                if segment.replacement:
                    aligned_second_superwitness.append(
                        ("replaced", str(tokens_witness_a) + " -> " + str(tokens_witness_b)))
                elif segment.addition:
                    aligned_second_superwitness.append(("+", str(tokens_witness_b)))
                else:
                    # segment is omission
                    aligned_second_superwitness.append(("-", str(tokens_witness_a)))
            # else it is aligned
            else:
                aligned_second_superwitness.append(("aligned", str(tokens_witness_a), str(tokens_witness_b)))
        return aligned_second_superwitness


    def add_superwitness_to_tree(self, segmented_superwitness):
        root = Node(None)
        for segment in segmented_superwitness:
            node = Node(segment)
            root.add_child(node)
        return root


    # def two_step_alignment(self, tokens_a, tokens_b):
    #     content_segmented_superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
    #     input_second_alignment = []
    #     for segment in content_segmented_superwitness:
    #         # segment is a tuple in a list; we check the first value of the tuple
    #         if segment.replacement:
    #             input_second_alignment.append(segment)
    #     # take this as input to realign tokens
    #     if not input_second_alignment:
    #         return content_segmented_superwitness
    #     else:
    #         type_segments = {}
    #         for segment in input_second_alignment:
    #             tokens_a, tokens_b = segment.tokens
    #             type_segmented_superwitness = align_tokens_on_type_and_return_superwitness(tokens_a, tokens_b)
    #             type_segments[segment] = type_segmented_superwitness
    #     print(type_segments)