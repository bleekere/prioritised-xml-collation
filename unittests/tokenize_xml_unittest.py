import unittest

from prioritised_xml_collation.tokenizer import Tokenizer


class TokenizeXML(unittest.TestCase):
    def test_tokenize_xml(self):
        input = open("../input_xml/witA-simple.xml")
        tokenizer = Tokenizer()
        tokens = str(tokenizer.convert_xml_file_into_tokens(input))
        # tokens are returned as a list
        # and list is stringified in order to test
        expected = "[TEI, s, The, add, black, /add, cat, ., /s, /TEI]"
        self.assertEqual(expected, tokens)