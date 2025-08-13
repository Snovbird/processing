from common.common import dropdown,msgbox
import ast

string_lists = ["['NA', -1]", "['OK', 1]", "['ERROR', 0]"]
actual_lists = [ast.literal_eval(s) for s in string_lists]
print(actual_lists)  # [['NA', -1], ['OK', 1], ['ERROR', 0]]
