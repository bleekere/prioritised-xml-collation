import unittest

from prioritised_xml_collation.tokenizer import convert_xml_file_into_tokens


class TokenizeText(unittest.TestCase):
    def test_text_tokens(self):
        xml_filename = open("../input_xml/witA-s021-simple.xml")
        # create list of token objects from input
        tokenized_input = convert_xml_file_into_tokens(xml_filename)
        # transform list of tokens to list of strings because it is easier to test
        list_tokens_string = [(str(token)) for token in tokenized_input]
        expected = ['Hoe', 'zoet', 'moet', 'nochtans', 'zijn', 'dit', 'werven', 'om', 'trachten', 'naar', 'een', 'vrouw', ',', 'de', 'ongewisheid', 'vóór', 'de', 'liefelijke', 'toestemming', '!']
        self.assertEqual(expected, list_tokens_string)