import re

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"

def create_ast(rule_string):
    def parse_expression(expr):
        tokens = re.findall(r'(\b\w+\b|[><=]+|\(|\)|\band\b|\bor\b)', expr)
        stack = []

        def get_priority(op):
            if op in ('and', 'or'):
                return 1
            if op in ('>', '<', '>=', '<=', '=', '!='):
                return 2
            return 0

        def apply_operator(operators, values):
            operator = operators.pop()
            right = values.pop()
            left = values.pop()
            values.append(Node(type='operator', left=left, right=right, value=operator))

        values = []
        operators = []
        for token in tokens:
            if token.isdigit() or re.match(r"'[^']*'", token):
                values.append(Node(type='operand', value=token))
            elif token.isidentifier():
                values.append(Node(type='operand', value=token))
            elif token in ('>', '<', '>=', '<=', '=', '!='):
                while (operators and get_priority(operators[-1]) >= get_priority(token)):
                    apply_operator(operators, values)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()
            elif token in ('and', 'or'):
                while (operators and get_priority(operators[-1]) >= get_priority(token)):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            apply_operator(operators, values)

        return values[0]

    return parse_expression(rule_string)

def evaluate_ast(ast, data):
    def evaluate_node(node):
        if node.type == 'operand':
            if re.match(r"'[^']*'", node.value):
                return node.value.strip("'")
            elif node.value.isdigit():
                return int(node.value)
            else:
                return data.get(node.value)
        elif node.type == 'operator':
            left = evaluate_node(node.left)
            right = evaluate_node(node.right)
            if node.value == 'and':
                return left and right
            elif node.value == 'or':
                return left or right
            elif node.value == '>':
                return left > right
            elif node.value == '<':
                return left < right
            elif node.value == '>=':
                return left >= right
            elif node.value == '<=':
                return left <= right
            elif node.value == '=':
                return left == right
            elif node.value == '!=':
                return left != right

    return evaluate_node(ast)
