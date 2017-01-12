import unittest

from prioritised_xml_collation.EditGraphAligner import EditGraphAligner
from prioritised_xml_collation.coordination import align_tokens_and_return_superwitness
from prioritised_xml_collation.tokenizer import Tokenizer


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
        expected = ['Hoe, zoet, moet, nochtans, zijn, dit, werven, om, trachten, naar, een, vrouw',
                    "['-,', '-de', '-ongewisheid']->['+!', '+Die', '+dagen', '+van', '+nerveuze', '+verwachting']",
                    'vóór, de, liefelijke, toestemming', "['-!']->['+.']"]
        self.assertEqual(expected, list_superwitness_string)

    def test_superwitness_segmentation(self):
        witA = open("/Users/ellibleeker/PycharmProjects/prioritised_xml_collation/input_xml/witA-s021-simple.xml")
        witB = open("/Users/ellibleeker/PycharmProjects/prioritised_xml_collation/input_xml/witB-s021-simple.xml")
        tokenizer = Tokenizer()
        tokens_a = tokenizer.convert_xml_file_into_tokens(witA)
        tokens_b = tokenizer.convert_xml_file_into_tokens(witB)
        # get results of segmented superwitness from method below
        segmented_superwitness = self.refine_segments_of_superwitness(tokens_a, tokens_b)
        # exptected output is a tuple of two values:
        # a string representation of the edit operation
        # and a string representation of the token concent
        expected = [("aligned", "[Hoe, zoet, moet, nochtans, zijn, dit, werven, om, trachten, naar, een, vrouw]"),
                    ("replaced", "[,, de, ongewisheid] -> [!, Die, dagen, van, nerveuze, verwachting]"),
                    ("aligned", "[vóór, de, liefelijke, toestemming]"), ("replaced", "[!] -> [.]")]
        self.assertEqual(expected, segmented_superwitness)

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
                elif segment.omission:
                    segmented_superwitness.append(("-", str(tokens_witness_a)))
            # else it is aligned:
            else:
                segmented_superwitness.append(("aligned", str(tokens_witness_a)))
        return segmented_superwitness
