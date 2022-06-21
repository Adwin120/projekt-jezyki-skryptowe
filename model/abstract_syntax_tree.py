from dataclasses import dataclass
from typing import Literal, Callable, Mapping, TypeVar

T = TypeVar('T')

OPERAND_PRECEDENCE = 100
BRACKET_PRECEDENCE = 1


@dataclass
class OperatorProps:
    associativity: Literal['left', 'right']
    arity: Literal[1, 2]
    precedence: int
    callback: Callable[[T], T] | Callable[[T, T], T]


class Node:
    def __init__(self, value) -> None:
        self.left = None
        self.right = None
        self.parent = None
        self.value = value


class AbstractSyntaxTree:
    def __init__(self, operators: Mapping[str, OperatorProps], tokenizer: Callable[[str], list[str]],
                 operand_parser) -> None:
        self.operators = operators
        self.tokenizer = tokenizer
        self.root: Node | None = None
        self.currentNode: Node | None = None
        self.operand_parser = operand_parser

    def precedence(self, token: str):
        if token == '(' or token == ')':
            return BRACKET_PRECEDENCE
        if token in self.operators:
            return self.operators[token].precedence
        return OPERAND_PRECEDENCE

    def post_order_traversal(self, node: Node):
        if node is not None:
            yield from self.post_order_traversal(node.left)
            yield from self.post_order_traversal(node.right)
            yield node.value

    def exec(self):
        stack = []
        # print(list(self.post_order_traversal(self.root)))
        for token in self.post_order_traversal(self.root):
            if token not in self.operators:
                stack.append(self.operand_parser(token))
                continue

            props = self.operators[token]
            if props.arity == 1:
                x = stack.pop()
                stack.append(props.callback(x))
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(props.callback(a, b))

        return stack[0]

    def evaluate(self, expression: str):
        tokens = self.tokenizer(expression)
        self.root = Node('(')
        self.currentNode = self.root
        for token in tokens:
            self.add(token)

        self.add(')')
        return self.exec()

    def add(self, token):
        is_operator = token in self.operators
        props = None
        if is_operator:
            props = self.operators[token]

        climb = is_operator and props.arity == 1 and props.associativity == 'left'
        climb = climb or token == '('
        climb = not climb

        if climb:
            while self.precedence(self.currentNode.value) > self.precedence(token):
                if self.currentNode.parent is None:
                    break
                self.currentNode = self.currentNode.parent

        climb_more = is_operator and props.arity == 2 and props.associativity == 'right'
        climb_more = climb_more or token == ')'
        climb_more = not climb_more
        climb_more = climb_more and climb

        if climb_more:
            while self.precedence(self.currentNode.value) == self.precedence(token):
                if self.currentNode.parent is None:
                    break
                self.currentNode = self.currentNode.parent

        if token == ')':
            if self.currentNode.parent is None:
                self.root = self.root.right
            else:
                self.currentNode.parent.right = self.currentNode.right
                self.currentNode.right.parent = self.currentNode.parent
                self.currentNode = self.currentNode.parent

        else:
            new_node = Node(token)
            new_node.left = self.currentNode.right
            if self.currentNode.right is not None:
                self.currentNode.right.parent = new_node
            self.currentNode.right = new_node
            new_node.parent = self.currentNode
            self.currentNode = new_node
