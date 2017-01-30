from hamcrest.core.base_matcher import BaseMatcher

from prioritised_xml_collation.tokenizer import TextToken, Token


class TokenContentMatcher(BaseMatcher):
    def __init__(self, expected_token):
        self.expected_token = expected_token

    # check if given item has content field
    def _matches(self, item):
        if not isinstance(item, Token):
            return False
        # if item has content field, check if content matches
        return item.content == self.expected_token.content

    def describe_to(self, description):
        description.append_text("Expected content to be " + self.expected_token.content + ".")
        # mismatch_description.append_text("but token has" + item.content + "instead.")

def token_content(expected_content):
    expected_token = Token(expected_content)
    return TokenContentMatcher(expected_token)