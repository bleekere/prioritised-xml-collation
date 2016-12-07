import unittest

from prioritised_xml_collation.tokenizer import tokenize_text, convert_xml_file_into_tokens


class ParentTextToken(unittest.TestCase):
    def test_find_your_parent(self):
        xml_filename = open(
            "/Users/ellibleeker/PycharmProjects/prioritised_xml_collation/input_xml/witA-s021-simple.xml")
        # create list of token objects from input
        tokenized_input = convert_xml_file_into_tokens(xml_filename)
        token_list = [(token.content, token.annot_info.tag_name) for token in tokenized_input]
        expected = [('Hoe', 's'), ('zoet', 's'), ('moet', 's'), ('nochtans', 's'), ('zijn', 's'), ('dit', 's'),
                    ('werven', 'del'), ('om', 'del'), ('trachten', 'add'), ('naar', 'add'), ('een', 's'),
                    ('vrouw', 's'), (',', 's'), ('de', 's'), ('ongewisheid', 's'), ('vóór', 's'), ('de', 's'),
                    ('liefelijke', 's'), ('toestemming', 's'), ('!', 's')]
        self.assertEqual(expected, token_list)

# define that this tag is an XML tag w/ START_ELEMENT
#  parse XML doc and store information of first parent of text token in AnnotationInformation object

# convert xml document into tokens
