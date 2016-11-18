import re
import unittest
from xml.dom.minidom import getDOMImplementation
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parse, END_ELEMENT, parseString


# - make Token object
# - Traverse the xml file of witness and take out all text characters
# - Whitespace normalisation
# - Tokenise the text characters on whitespace
# - Return list of tokens

class TextToken(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


# parse xml file
def convert_xml_file_into_tokens(xml_filename):
    doc = parse(xml_filename)
    return convert_xml_doc_into_tokens(doc)


# convert xml document into tokens
def convert_xml_doc_into_tokens(xml_doc):
    tokens = []
    for event, node in xml_doc:
        if event == CHARACTERS:
            tokens.extend(tokenize_text(node.data))

        elif event == START_ELEMENT:
            pass

        elif event == END_ELEMENT:
            pass
    return tokens


# tokenize text
# data adds text to current element; data is a string
def tokenize_text(data):
    return (TextToken(content) for content in re.findall(r'\w+|[^\w\s]+', data))
# returns list of text token objects


class TokenizeText(unittest.TestCase):
    def test_text_tokens(self):
        xml_filename = open("/Users/ellibleeker/PycharmProjects/xml_collation/bin-ignore/witA-s021-simple.xml")
        # create list of token objects from input
        tokenized_input = convert_xml_file_into_tokens(xml_filename)
        # transform list of tokens to list of strings because it is easier to test
        list_tokens_string = [(str(token)) for token in tokenized_input]
        expected = ['Hoe', 'zoet', 'moet', 'nochtans', 'zijn', 'dit', 'werven', 'om', 'trachten', 'naar', 'een', 'vrouw', ',', 'de', 'ongewisheid', 'vóór', 'de', 'liefelijke', 'toestemming', '!']
        self.assertEqual(expected, list_tokens_string)
