from hamcrest.core.base_matcher import BaseMatcher

from prioritised_xml_collation.tokenizer import TextToken, Token


class TokenContent(BaseMatcher):
    def __init__(self, expected_token):
        self.expected_token = expected_token

    # check if given item has content field
    def _matches(self, item):
        print(str(item))
        if not isinstance(item, Token):
            return False
        # if item has content field, check if content matches
        return item.content == self.expected_token.content

    def describe_to(self, description):
        description.append_text("Expected content to be " + self.expected_token.content + ".")
        # mismatch_description.append_text("but token has" + item.content + "instead.")

def token_content(expected_text):
    content_token = Token(expected_text)
    return TokenContent(content_token)