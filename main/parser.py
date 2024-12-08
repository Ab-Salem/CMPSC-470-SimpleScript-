from lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = []
        self.position = 0

    def consume(self, expected_type=None):
        if self.position < len(self.tokens):
            token_type, value = self.tokens[self.position]
            if expected_type and token_type != expected_type:
                raise SyntaxError(f"Expected {expected_type}, got {token_type} ({value})")
            self.position += 1
            return value
        return None

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def parse_statement(self):
        if self.position >= len(self.tokens):
            return None

        token_type, value = self.tokens[self.position]
        if token_type == "ASSIGNMENT" and value == "set":
            return self.parse_assignment()
        elif token_type == "IDENTIFIER" and value == "print":
            return self.parse_print()
        elif token_type == "ASSIGNMENT" and value == "read":
            return self.parse_read()
        else:
            raise SyntaxError(f"Unexpected token: {value}")

    def parse_assignment(self):
        self.consume("ASSIGNMENT")  # Consume 'set'
        variable = self.consume("IDENTIFIER")
        if not variable:
            raise SyntaxError("Expected variable name after 'set'")
        self.consume("ASSIGNMENT")  # Consume 'to'
        expression = self.parse_expression()
        if not expression:
            raise SyntaxError("Expected expression after 'to'")
        return {
            "type": "assignment",
            "variable": variable,
            "value": expression
        }

    def parse_read(self):
        """Parse a read file statement."""
        self.consume("ASSIGNMENT")  # Consume 'read'
        filename = self.parse_expression()
        if not filename:
            raise SyntaxError("Expected filename after 'read'")
        return {
            "type": "read_file",
            "filename": filename
        }
    
    def parse_print(self):
        self.consume("IDENTIFIER")  # Consume 'print'
        expression = self.parse_expression()
        if not expression:
            raise SyntaxError("Expected expression after 'print'")
        return {
            "type": "print",
            "value": expression
        }

    def parse_expression(self):
        left = self.parse_term()
        if not left:
            return None
        while self.peek() and self.peek()[0] == "ARITHMETIC":
            operator = self.consume("ARITHMETIC")
            right = self.parse_term()
            if not right:
                raise SyntaxError("Expected expression after operator")
            left = {
                "type": "binary_operation",
                "operator": operator,
                "left": left,
                "right": right
            }
        return left

    def parse_term(self):
        if self.position >= len(self.tokens):
            return None
        token_type, value = self.tokens[self.position]
        if token_type in {"NUMBER", "STRING", "IDENTIFIER"}:
            self.consume(token_type)
            return {
                "type": token_type.lower(),
                "value": value
            }
        return None

    def run(self, text):
        try:
            # Tokenize and reset state for each input
            self.tokens = self.lexer.tokenize(text)
            self.position = 0
            ast = self.parse_statement()
            return ast, None
        except SyntaxError as e:
            return None, str(e)
