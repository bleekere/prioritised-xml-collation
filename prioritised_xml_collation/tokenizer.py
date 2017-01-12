import re
import unittest
from xml.dom.minidom import getDOMImplementation
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parse, END_ELEMENT, parseString
from collections import namedtuple, defaultdict


# - make Token object
# - Traverse the xml file of witness and take out all text characters
# - Whitespace normalisation
# - Tokenise the text characters on whitespace
# - Return list of tokens

class Token(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


class TextToken(Token):
    def __init__(self, content):
        super(TextToken, self).__init__(content)


class ElementToken(Token):
    pass


class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]


class Tokenizer(object):
    def convert_xml_string_into_tokens(self, xml_string):
        # string is in memory
        xml = parseString(xml_string)
        return self.convert_xml_into_tokens(xml)

    def convert_xml_file_into_tokens(self, xml_filename):
        xml = parse(xml_filename)
        return self.convert_xml_into_tokens(xml)

    def convert_xml_into_tokens(self, xml):
        # xml is a stream of xml characters,
        # which can come in the form of a string or in the form of a file
        # init output
        # NOTE: tokens objects are made so to make them unique (localName can be repeated)
        # NOTE: we might want to make the tokens more complex to store the original location in xpath form
        tokens = []
        for event, node in xml:
            # debug
            # print(event, node)
            if event == CHARACTERS:
                tokens.extend(self.tokenize_text(node.data))

            elif event == START_ELEMENT:
                tokens.append(ElementToken(node.localName))

            elif event == END_ELEMENT:
                tokens.append(ElementToken("/" + node.localName))
        return tokens

    # tokenize text
    # data adds text to current element; data is a string
    def tokenize_text(self, data):
        return (TextToken(content) for content in re.findall(r'\w+|[^\w\s]+', data))


# returns list of text token objects



