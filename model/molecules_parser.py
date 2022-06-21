import re

from model.abstract_syntax_tree import OperatorProps, AbstractSyntaxTree


def sum_atoms(a, b):
    a = a.copy()
    for key in a.keys():
        a[key] += b.get(key, 0)
    return b | a


def multiply_atoms(a, n):
    a = a.copy()
    for key in a.keys():
        a[key] *= n
    return a


OPERATORS = {
    '+': OperatorProps('left', 2, 20, sum_atoms),
    '*': OperatorProps('right', 2, 40, multiply_atoms)
}


def atom_parser(str):
    if str.isnumeric():
        return float(str)
    return {
        str: 1
    }


def atom_tokenizer(expression: str):
    tokens = re.findall(r'[A-Z][a-z]*|\d+|[()]', expression)
    tokens_with_operators = [tokens[0]]
    for i in range(1, len(tokens)):
        if (not tokens[i - 1].isnumeric()) and tokens[i].isnumeric():
            tokens_with_operators.append('*')
        elif tokens[i - 1] != '(' and not tokens[i].isnumeric() and tokens[i] != ')':
            tokens_with_operators.append('+')
        tokens_with_operators.append(tokens[i])
    return tokens_with_operators


ast = AbstractSyntaxTree(OPERATORS, atom_tokenizer, atom_parser)

def evaluate_molecule(expression: str):
    return ast.evaluate(expression)