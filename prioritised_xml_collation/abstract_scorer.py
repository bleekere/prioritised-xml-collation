from abc import ABC, abstractmethod

class Scorer(ABC):
    @abstractmethod
    def score_cell(self, table_node, parent_node, token_a, token_b, y, x, edit_operation):
        # no matching possible in this case (always treated as a gap)
        # it is either an add or a delete
        if x == 0 or y == 0:
            table_node.g = parent_node.g - 1
            return
        # we score differently depending on the type of edit operation
        # edit operation 0: it is either a match or a replacement (so an add and a delete)
        # edit operation 1: it is either an add/delete
        if edit_operation == 0:
            # it is a match or a replacement
            match = self.match(token_a, token_b)
            # print("testing "+token_a.token_string+" and "+token_b.token_string+" "+str(match))
            # match = token_a.token_string == token_b.token_string
            # based on match or not and parent_node calculate new score
            if match == 0:
                # mark the fact that this node is match
                table_node.match = True
                # do not change score for now
                table_node.g = parent_node.g
                # count segments
                if not parent_node.match:
                    table_node.segments = parent_node.segments + 1
                return
            if match == 1:
                # it is a near match
                table_node.g = parent_node.g - 0.5  # TODO: TEST TEST TEST
                pass
            else:
                # it is a replacement
                table_node.g = parent_node.g - 2
                return
        else:
            # it is a omission/addition
            table_node.g = parent_node.g - 1
            return

        # return values:
        # 0 = FULL_MATCH
        # -1 = NO MATCH
        # 1 = PARTIAL MATCH
    @abstractmethod
    def match(self, token_a, token_b):
        pass

