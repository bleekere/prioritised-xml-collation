import unittest
from collections import namedtuple

from prioritised_xml_collation.tokenizer import tokenize_text, convert_xml_file_into_tokens
# TODO update functionality and expected output


class ParentTextToken(unittest.TestCase):
    def test_find_your_parent_A(self):
        xml_filename = open(
            "../input_xml/witA-s021-simple.xml")
        # create list of token objects from input
        tokenized_input = convert_xml_file_into_tokens(xml_filename)
        token_list = [(token.content, token.annot_info.tag_name) for token in tokenized_input]
        expected = [('Hoe', 's'), ('zoet', 's'), ('moet', 's'), ('nochtans', 's'), ('zijn', 's'), ('dit', 's'),
                    ('werven', 'del'), ('om', 'del'), ('trachten', 'add'), ('naar', 'add'), ('een', 's'),
                    ('vrouw', 's'), (',', 's'), ('de', 's'), ('ongewisheid', 's'), ('vóór', 's'), ('de', 's'),
                    ('liefelijke', 's'), ('toestemming', 's'), ('!', 's')]
        self.assertEqual(expected, token_list)

    def test_find_your_parent_B(self):
        xml_filename = open(
            "../input_xml/witB-s021-simple.xml")
        # create list of token objects from input
        tokenized_input = convert_xml_file_into_tokens(xml_filename)
        token_list = [(token.content, token.annot_info.tag_name) for token in tokenized_input]
        expected = [('Hoe', 's'), ('zoet', 's'), ('moet', 's'), ('nochtans', 's'), ('zijn', 's'), ('dit', 's'),
                    ('werven', 'del'), ('om', 'del'), ('trachten', 'add'), ('naar', 'add'), ('een', 's'),
                    ('vrouw', 's'), ('!', 's'), ('Die', 's'), ('dagen', 's'), ('van', 's'), ('nerveuze', 's'),
                    ('verwachting', 's'), ('vóór', 's'), ('de', 's'),
                    ('liefelijke', 's'), ('toestemming', 's'), ('.', 's')]
        self.assertEqual(expected, token_list)

    def test_find_your_real_parent_B(self):
        xml_filename = open(
            "../input_xml/witB-s021-simple.xml")
        # create list of token objects from input
        tokenized_input = convert_xml_file_into_tokens(xml_filename)
        # assert whether annot_info of item 0 == annot_info of item 10
        self.assertEqual(tokenized_input[0].annot_info, tokenized_input[10].annot_info)
        # assert whether annot_info of item 0 != annot_info of item 13
        self.assertFalse(tokenized_input[0].annot_info == tokenized_input[13].annot_info)




