import unittest

from prioritised_xml_collation.TextGraph import convert_superwitness_to_textgraph
from prioritised_xml_collation.tokenizer import convert_xml_file_into_tokens
from unittests.alignment_text_tokens_unittest import align_tokens_and_return_superwitness
# TODO update functionality and expected output


# from prioritised_xml_collation.text_graph_exporter import export_as_dot

class TextGraph(unittest.TestCase):
    def test_text_graph(self):
        witA = open("/Users/ellibleeker/PycharmProjects/prioritised_xml_collation/input_xml/witA-s021-simple.xml")
        witB = open("/Users/ellibleeker/PycharmProjects/prioritised_xml_collation/input_xml/witB-s021-simple.xml")
        tokens_a = convert_xml_file_into_tokens(witA)
        tokens_b = convert_xml_file_into_tokens(witB)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        text_tokens = textgraph.text_tokens
        self.assertEquals("[Hoe, zoet, moet, nochtans, zijn, dit, werven, om, trachten, naar, een, vrouw, -,, -de, -ongewisheid, +!, +Die, +dagen, +van, +nerveuze, +verwachting, vóór, de, liefelijke, toestemming, -!, +.]", str(text_tokens))



# class TextGraph(unittest.TestCase):
#     def test_text_graph(self):
#         witA = open("input_xml/witA-s021-simple.xml")
#         witB = open("input_xml/witB-s021-simple.xml")
#         tokens_a = convert_xml_file_into_tokens(witA)
#         tokens_b = convert_xml_file_into_tokens(witB)
#         superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
#         textgraph = convert_superwitness_to_textgraph(superwitness)
#         dot_export = export_as_dot(textgraph)
#         expected_out = """strict digraph TextGraph {
#             1 [label="Hoe"]
#             2 [label="zoet"]
#             3 [label="moet"]
#             4 [label="nochtans"]
#             5 [label="zijn"]
#             6 [label="dit"]
#             7 [label="werven"]
#             8 [label="om"]
#             9 [label="trachten"]
#             10 [label="naar"]
#             11 [label="een"]
#             12 [label="vrouw"]
#             13 [label=","]
#             14 [label="de"]
#             15 [label="ongewisheid"]
#             16 [label="!"]
#             17 [label="Die"]
#             18 [label="dagen"]
#             19 [label="van"]
#             20 [label="nerveuze"]
#             21 [label="verwachting"]
#             22 [label="voor"]
#             23 [label="de"]
#             24 [label="liefelijke"]
#             25 [label="toestemming"]
#             26 [label="!"]
#             27 [label="."]
#
#             1 -> 2
#             2 -> 3
#             3 -> 4
#             4 -> 5
#
#         { rank=same; 1; 2; 3 }
#         }"""
#         self.assertEqual(expected_out, dot_export)