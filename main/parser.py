# parser.py
from lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = []
        self.position = 0
        self.in_function = False

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

    def peek_next(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def consume_if_matches(self, expected_type, expected_value):
        if self.peek() and self.peek()[0] == expected_type and self.peek()[1] == expected_value:
            self.consume(expected_type)
            return True
        return False

    def parse_statement(self):
        if self.position >= len(self.tokens):
            return None

        token_type, value = self.tokens[self.position]
        
        if token_type == "KEYWORD":
            if value == "if":
                return self.parse_if_statement()
            elif value == "while":
                return self.parse_while_statement()
            elif value == "function":
                return self.parse_function_definition()
            elif value == "return":
                return self.parse_return_statement()
            elif value == "ask":
                return self.parse_ask()
            elif value == "group":
                return self.parse_group_creation()
        elif token_type == "ASSIGNMENT" and value == "set":
            return self.parse_assignment()
        elif token_type == "IDENTIFIER":
            if value == "print":
                return self.parse_print()
            next_token = self.peek_next()
            if next_token:
                if next_token[1] == "(":
                    return self.parse_function_call()
                elif next_token[1] == "[":
                    return self.parse_group_operation()
        elif token_type == "ASSIGNMENT" and value == "read":
            return self.parse_read()
            
        raise SyntaxError(f"Unexpected token: {value}")

    def parse_expression(self):
        left = self.parse_comparison()
        if not left:
            return None
            
        while self.peek() and self.peek()[0] == "LOGICAL":
            operator = self.consume("LOGICAL")
            right = self.parse_comparison()
            if not right:
                raise SyntaxError("Expected expression after logical operator")
            left = {
                "type": "logical_operation",
                "operator": operator,
                "left": left,
                "right": right
            }
        return left

    def parse_comparison(self):
        left = self.parse_arithmetic()
        if not left:
            return None
            
        while self.peek() and self.peek()[0] == "COMPARISON":
            operator = self.consume("COMPARISON")
            right = self.parse_arithmetic()
            if not right:
                raise SyntaxError("Expected expression after comparison operator")
            left = {
                "type": "comparison_operation",
                "operator": operator,
                "left": left,
                "right": right
            }
        return left

    def parse_arithmetic(self):
        left = self.parse_term()
        if not left:
            return None
            
        while self.peek() and self.peek()[0] == "ARITHMETIC":
            operator = self.consume("ARITHMETIC")
            right = self.parse_term()
            if not right:
                raise SyntaxError("Expected expression after arithmetic operator")
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
        if token_type in {"NUMBER", "STRING", "IDENTIFIER", "BOOLEAN"}:
            self.consume(token_type)
            if token_type == "BOOLEAN":
                return {
                    "type": "boolean",
                    "value": value.lower() == "true"
                }
            return {
                "type": token_type.lower(),
                "value": value
            }
        return None

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

    def parse_if_statement(self):
        self.consume("KEYWORD")  # Consume 'if'
        condition = self.parse_expression()
        if not self.consume_if_matches("KEYWORD", "then"):
            raise SyntaxError("Expected 'then' after if condition")
            
        then_block = self.parse_block()
        else_block = None
        
        if self.peek() and self.peek()[1] == "else":
            self.consume("KEYWORD")  # Consume 'else'
            else_block = self.parse_block()
            
        if not self.consume_if_matches("KEYWORD", "end"):
            raise SyntaxError("Expected 'end' after if statement")
            
        return {
            "type": "if_statement",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block
        }

    def parse_while_statement(self):
        self.consume("KEYWORD")  # Consume 'while'
        condition = self.parse_expression()
        if not self.consume_if_matches("KEYWORD", "do"):
            raise SyntaxError("Expected 'do' after while condition")
            
        body = self.parse_block()
        
        if not self.consume_if_matches("KEYWORD", "end"):
            raise SyntaxError("Expected 'end' after while loop")
            
        return {
            "type": "while_statement",
            "condition": condition,
            "body": body
        }

    def parse_function_definition(self):
        self.consume("KEYWORD")  # Consume 'function'
        name = self.consume("IDENTIFIER")
        if not name:
            raise SyntaxError("Expected function name")
            
        if not self.consume_if_matches("SYMBOL", "("):
            raise SyntaxError("Expected '(' after function name")
            
        parameters = []
        while self.peek() and self.peek()[1] != ")":
            if parameters:
                if not self.consume_if_matches("SYMBOL", ","):
                    raise SyntaxError("Expected ',' between parameters")
            param = self.consume("IDENTIFIER")
            if not param:
                raise SyntaxError("Expected parameter name")
            parameters.append(param)
            
        if not self.consume_if_matches("SYMBOL", ")"):
            raise SyntaxError("Expected ')' after parameters")
            
        self.in_function = True
        body = self.parse_block()
        self.in_function = False
        
        if not self.consume_if_matches("KEYWORD", "end"):
            raise SyntaxError("Expected 'end' after function body")
            
        return {
            "type": "function_definition",
            "name": name,
            "parameters": parameters,
            "body": body
        }

    def parse_return_statement(self):
        if not self.in_function:
            raise SyntaxError("Return statement outside function")
            
        self.consume("KEYWORD")  # Consume 'return'
        value = self.parse_expression()
        
        return {
            "type": "return_statement",
            "value": value
        }

    def parse_function_call(self):
        name = self.consume("IDENTIFIER")
        self.consume("SYMBOL")  # Consume '('
        
        arguments = []
        while self.peek() and self.peek()[1] != ")":
            if arguments:
                if not self.consume_if_matches("SYMBOL", ","):
                    raise SyntaxError("Expected ',' between arguments")
            arg = self.parse_expression()
            if not arg:
                raise SyntaxError("Expected argument")
            arguments.append(arg)
            
        if not self.consume_if_matches("SYMBOL", ")"):
            raise SyntaxError("Expected ')' after arguments")
            
        return {
            "type": "function_call",
            "name": name,
            "arguments": arguments
        }

    def parse_block(self):
        statements = []
        while self.peek() and not (self.peek()[0] == "KEYWORD" and 
              self.peek()[1] in ["end", "else"]):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements

    def parse_ask(self):
        self.consume("KEYWORD")  # Consume 'ask'
        prompt = self.parse_expression()
        if not prompt:
            raise SyntaxError("Expected prompt expression after 'ask'")
        return {
            "type": "ask",
            "prompt": prompt
        }

    def parse_group_creation(self):
        self.consume("KEYWORD")  # Consume 'group'
        
        if not self.consume_if_matches("SYMBOL", "["):
            raise SyntaxError("Expected '[' after 'group'")
            
        elements = []
        while self.peek() and self.peek()[1] != "]":
            if elements:
                if not self.consume_if_matches("SYMBOL", ","):
                    raise SyntaxError("Expected ',' between group elements")
            element = self.parse_expression()
            if not element:
                raise SyntaxError("Expected expression in group")
            elements.append(element)
            
        if not self.consume_if_matches("SYMBOL", "]"):
            raise SyntaxError("Expected ']' after group elements")
            
        return {
            "type": "group_creation",
            "elements": elements
        }

    def parse_group_operation(self):
        name = self.consume("IDENTIFIER")
        self.consume("SYMBOL")  # Consume '['
        index = self.parse_expression()
        
        if not self.consume_if_matches("SYMBOL", "]"):
            raise SyntaxError("Expected ']' after index")
            
        next_token = self.peek()
        if next_token and next_token[0] == "ASSIGNMENT" and next_token[1] == "to":
            self.consume("ASSIGNMENT")  # Consume 'to'
            value = self.parse_expression()
            return {
                "type": "group_assignment",
                "name": name,
                "index": index,
                "value": value
            }
            
        return {
            "type": "group_access",
            "name": name,
            "index": index
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

    def parse_read(self):
        self.consume("ASSIGNMENT")  # Consume 'read'
        filename = self.parse_expression()
        if not filename:
            raise SyntaxError("Expected filename after 'read'")
        return {
            "type": "read_file",
            "filename": filename
        }

    def run(self, text):
        try:
            self.tokens = self.lexer.tokenize(text)
            self.position = 0
            ast = self.parse_statement()
            return ast, None
        except SyntaxError as e:
            return None, str(e)