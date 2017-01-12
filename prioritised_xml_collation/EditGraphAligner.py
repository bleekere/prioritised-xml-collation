"""
    EditGraphAligner
    @author: Ronald Haentjens Dekker
    This class uses dynamic programming to find the optimal alignment between
    two lists of strings/tokens given a certain scoring function.
"""
from typing import Tuple, List

from prioritised_xml_collation.exact_match_scorer import TextScorer
from prioritised_xml_collation.tokenizer import Token


class EditGraphNode(object):
    def __init__(self):
        self.g = 0 # global score
        self.segments = 0 # number of segments
        self.match = False # this node represents a match or not

    def __repr__(self):
        return repr(self.g)


class Segment(object):
    def __init__(self, tokens: Tuple[List[Token], List[Token]], aligned, addition, replacement):
        # the field self.tokens is a tuple of two list of token objects
        # TODO look at complexity of parameter 'tokens' and consider a simpler parameter
        self.tokens = tokens
        self.aligned = aligned
        self.addition = addition
        self.replacement = replacement

    @property
    def witnesses(self):
        if self.aligned:
            return ["A", "B"]
        elif self.addition:
            return ["B"]
        else:
            # TODO: add unit test for this specific case (omission)
            return ["A"]

    def __str__(self):
        # call the informal 'nicely printable' string representation of the object
        return repr(self)

    def __repr__(self):
        # call the official string representation of the object
        prefix = ""
        if not self.aligned:
            # self.tokens is a tuple so define which element we need
            if self.addition:
                return str(["+" + str(token) for token in self.tokens[1]])
            if self.replacement:
                tokens_witness_a, tokens_witness_b = self.tokens
                return str(["-" + str(token) for token in tokens_witness_a]) + "->" + str(["+" + str(token) for token in tokens_witness_b])
            else:
                return str(["-" + str(token) for token in self.tokens[0]])
        return ", ".join([str(token) for token in self.tokens[0]])


class ExtendedToken(object):
    def __init__(self, token, aligned, addition):
        self.token = token
        self.aligned = aligned
        self.addition = addition

    @property
    def witnesses(self):
        if self.aligned:
            return ["A", "B"]
        elif self.addition:
            return ["B"]
        else:
            # TODO: add unit test for this specific case (omission)
            return ["A"]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        prefix = ""
        if not self.aligned:
            if self.addition:
                prefix += "+"
            else:
                prefix += "-"
        return ", ".join([prefix + self.token.content])


class EditGraphAligner(object):
    def __init__(self):
        self.scorer = TextScorer()

    def align(self, tokens_witness_a, tokens_witness_b):
        self.tokens_witness_a = tokens_witness_a
        self.tokens_witness_b = tokens_witness_b
        self.length_witness_a = len(self.tokens_witness_a)
        self.length_witness_b = len(self.tokens_witness_b)

        # clear table: fill table with empty nodes
        # Note: in a large table this init takes a lot of time
        self.table = [[EditGraphNode() for _ in range(self.length_witness_a+1)] for _ in range(self.length_witness_b+1)]

        # per diagonal calculate the score (taking into account the three surrounding nodes)
        self.traverse_table_diagonally(self.score_cell)

        alignment = self.calculate_alignment_and_superwitness()
        return alignment

    def calculate_alignment_and_superwitness(self):
        alignment = {}
        # note we traverse from right to left!
        self.last_x = self.length_witness_a
        self.last_y = self.length_witness_b
        self.superwitness = []
        # start lower right cell
        x = self.length_witness_a
        y = self.length_witness_b
        # work our way to the upper left
        while x > 0 and y > 0:
            self._process_cell(self.tokens_witness_a, self.tokens_witness_b, alignment, x, y)
            # examine neighbor nodes
            nodes_to_examine = set()
            # table is a list of lists
            # [x] and [y] are used for coordinates in the table
            nodes_to_examine.add(self.table[y][x - 1])
            nodes_to_examine.add(self.table[y - 1][x])
            nodes_to_examine.add(self.table[y - 1][x - 1])
            # calculate the maximum scoring parent node
            parent_node = max(nodes_to_examine, key=lambda x: x.g)
            # move position
            if self.table[y - 1][x - 1] == parent_node:
                # another match or replacement
                y -= 1
                x -= 1
            else:
                # check whether edit operation is an omission
                if self.table[y - 1][x] == parent_node:
                    y -= 1
                else:
                    # check whether edit operation is an addition
                    if self.table[y][x - 1] == parent_node:
                        x -= 1
        # process additions/omissions in the beginning of the witnesses
        cell = self.table[y][x]
        self.add_to_superwitness(cell, self.tokens_witness_a, self.tokens_witness_b, 0, 0)
        return alignment

    def _process_cell(self, witness_a, witness_b, alignment, x, y):
        cell = self.table[y][x]
        last_cell = self.table[self.last_y][self.last_x]
        state_change = cell.match is not last_cell.match
        # process segments
        if state_change is True:
            self.add_to_superwitness(cell, witness_a, witness_b, x, y)
            self.last_x = x
            self.last_y = y
        # process alignment
        if cell.match:
            token = witness_a[x-1]
            token2 = witness_b[y-1]
            alignment[token2] = token

        return cell

    def add_to_superwitness(self, cell, witness_a, witness_b, x, y):
        tokens_witness_a = witness_a[x:self.last_x]
        tokens_witness_b = witness_b[y:self.last_y]
        # self.superwitness is an empty list
        # with insert we insert the Segment object in the beginning of the list
        # if next cell is match, look at current cell:
        if cell.match:
            # we first check for replacement otherwise the tokens are duplicated in the superwitness
            # if replacement (= omission followed by addition)
            if tokens_witness_a and tokens_witness_b:
                self.superwitness.insert(0, Segment((tokens_witness_a, tokens_witness_b), False, False, True))
            # addition
            # tuple of one value: tokens_witness_b, None
            elif tokens_witness_b:
                self.superwitness.insert(0, Segment((None, tokens_witness_b), False, True, False))
            # omission
            elif tokens_witness_a:
                # print x, self.last_x, y, self.last_y
                self.superwitness.insert(0, Segment((tokens_witness_a, None), False, False, False))
        else:
            # current cell matches next cell
            # aligned
                self.superwitness.insert(0, Segment((tokens_witness_a, tokens_witness_b), True, False, False))


    # This function traverses the table diagonally and calls the supplied function for each cell.
    # Original function from Mark Byers; translated from C into Python.
    def traverse_table_diagonally(self, function_to_call):
        m = self.length_witness_b+1
        n = self.length_witness_a+1
        for _slice in range(0, m + n - 1, 1):
            z1 = 0 if _slice < n else _slice - n + 1
            z2 = 0 if _slice < m else _slice - m + 1
            j = _slice - z2
            while j >= z1:
                x = _slice - j
                y = j
                function_to_call(y, x)
                j -= 1

    def score_cell(self, y, x):
        # initialize root node score to zero (no edit operations have
        # been performed)
        if y == 0 and x == 0:
            self.table[y][x].g = 0
            return
        # examine neighbor nodes
        nodes_to_examine = set()
        # fetch existing score from the left node if possible
        if x > 0:
            nodes_to_examine.add(self.table[y][x-1])
        if y > 0:
            nodes_to_examine.add(self.table[y-1][x])
        if x > 0 and y > 0:
            nodes_to_examine.add(self.table[y-1][x-1])
        # instead of the three possible values of the node
        # calculate the maximum scoring parent node
        # we are looking for the highest scoring parent node
        parent_node = max(nodes_to_examine, key=lambda x: x.g)
        if parent_node == self.table[y-1][x-1]:
            edit_operation = 0
        else:
            edit_operation = 1
        token_a = self.tokens_witness_a[x-1]
        token_b = self.tokens_witness_b[y-1]
        self.scorer.score_cell(self.table[y][x], parent_node, token_a, token_b, y, x, edit_operation)


     # def _debug_edit_graph_table(self, table):
     #     # print the table horizontal
     #     x = PrettyTable()
     #     x.header=False
     #     for y in range(0, len(table)):
     #         cells = table[y]
     #         x.add_row(cells)
     #     # alignment can only be set after the field names are known.
     #     # since add_row sets the field names, it has to be set after x.add_row(cells)
     #     x.align="l"
     #     print(x)
     #     return x
