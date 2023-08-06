from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
    r"""
    schools         = (school_block / ws)+

    school_block    = school_header ws grade_block+ 
    grade_block     = grade_header ws name_header ws (number_name)+ ws score_header ws (number_score)+ ws? 

    school_header   = ~"^School = (.*)"m
    grade_header    = ~"^Grade = (\d+)"m
    name_header     = "Student number, Name"
    score_header    = "Student number, Score"

    number_name     = index comma name ws
    number_score    = index comma score ws

    comma           = ws? "," ws?

    index           = number+
    score           = number+

    number          = ~"\d+"
    name            = ~"[A-Z]\w+"
    ws              = ~"\s*"
    """
)


class SchoolVisitor(NodeVisitor):
    output, names = ([], [])
    current_school, current_grade = None, None

    def _getName(self, idx):
        for index, name in self.names:
            if index == idx:
                return name

    def generic_visit(self, node, visited_children):
        return node.text or visited_children

    def visit_school_header(self, node, children):
        self.current_school = node.match.group(1)

    def visit_grade_header(self, node, children):
        self.current_grade = node.match.group(1)
        self.names = []

    def visit_number_name(self, node, children):
        index, name = None, None
        for child in node.children:
            if child.expr.name == 'name':
                name = child.text
            elif child.expr.name == 'index':
                index = child.text

        self.names.append((index, name))

    def visit_number_score(self, node, children):
        index, score = None, None
        for child in node.children:
            if child.expr.name == 'index':
                index = child.text
            elif child.expr.name == 'score':
                score = child.text

        name = self._getName(index)

        # build the entire entry
        entry = (self.current_school, self.current_grade, index, name, score)
        self.output.append(entry)
