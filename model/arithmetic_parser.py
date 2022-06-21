from model.abstract_syntax_tree import OperatorProps, AbstractSyntaxTree
import math
import re

OPERATORS = {
    '+': OperatorProps('left', 2, 20, lambda a, b: a + b),
    '-': OperatorProps('left', 2, 20, lambda a, b: a - b),
    'neg': OperatorProps('left', 1, 60, lambda a: -a),
    'sin': OperatorProps('left', 1, 30, math.sin),
    'cos': OperatorProps('left', 1, 30, math.cos),
    'tan': OperatorProps('left', 1, 30, math.tan),
    'log': OperatorProps('left', 1, 30, math.log),
    'sqrt': OperatorProps('left', 1, 30, math.sqrt),
    'abs': OperatorProps('left', 1, 30, abs),
    '*': OperatorProps('left', 2, 40, lambda a, b: a * b),
    '/': OperatorProps('left', 2, 40, lambda a, b: a / b),
    '^': OperatorProps('right', 2, 50, lambda a, b: a ** b),
    '!': OperatorProps('right', 1, 60, math.factorial),
}


def arithmetic_tokenizer(expression: str):
    expression = expression.lower()
    tokens = re.findall(r'\d+(?:\.\d*)?|[\(\)+\-*/!^]|[a-z]+', expression)
    for i in range(0, len(tokens)):
        if tokens[i] == '-' and (tokens[i - 1] in OPERATORS or tokens[i - 1] == '(' or i == 0):
            tokens[i] = 'neg'
    return tokens


ast = AbstractSyntaxTree(OPERATORS, arithmetic_tokenizer, float)

def evaluate_arithmetic(expression: str):
    return ast.evaluate(expression)