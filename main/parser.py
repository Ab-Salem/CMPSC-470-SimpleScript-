from lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = []
        self.position = 0
        self.function_nesting = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def peek_next(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def consume(self, expected_type=None):
        if self.position < len(self.tokens):
            token_type, value = self.tokens[self.position]
            if expected_type and token_type != expected_type:
                raise SyntaxError(f"Expected {expected_type}, got {token_type} ({value})")
            self.position += 1
            return value
        return None

    def consume_if_matches(self, expected_type, expected_value):
        if self.peek() and self.peek()[0] == expected_type and self.peek()[1] == expected_value:
            self.consume(expected_type)
            return True
        return False

    def parse_statement(self):
        if not self.peek():
            return None

        token_type, value = self.peek()

        # Handle array index assignment first
        if token_type == "ASSIGNMENT" and value == "set":
            self.consume("ASSIGNMENT")  # Consume 'set'
            if not self.peek():
                raise SyntaxError("Expected identifier after 'set'")
                
            # Look ahead to see if this is an array index assignment
            identifier_token = self.peek()
            if identifier_token[0] == "IDENTIFIER":
                next_token = self.peek_next()
                if next_token and next_token[1] == "[":
                    # This is an array index assignment
                    return self.parse_group_assignment()
                else:
                    # This is a regular assignment
                    self.position -= 1  # Go back to 'set'
                    return self.parse_assignment()
                    
        # Handle other statement types
        elif token_type == "IDENTIFIER" and value == "print":
            self.consume("IDENTIFIER")
            return self.parse_print()
        elif token_type == "KEYWORD":
            if value == "function":
                self.consume("KEYWORD")
                self.function_nesting += 1
                return self.parse_function_definition()
            elif value == "if":
                self.consume("KEYWORD")
                return self.parse_if_statement()
            elif value == "while":
                self.consume("KEYWORD")
                return self.parse_while_statement()
            elif value == "return":
                if not self.function_nesting:
                    raise SyntaxError("Return statement outside function")
                self.consume("KEYWORD")
                return self.parse_return_statement()
            elif value == "group":
                return self.parse_group_creation()
        elif token_type == "IDENTIFIER":
            next_token = self.peek_next()
            if next_token:
                if next_token[1] == "(":
                    return self.parse_function_call()
                elif next_token[1] == "[":
                    return self.parse_group_operation()

        raise SyntaxError(f"Unexpected token: {value}")

    def parse_print(self):
        value = self.parse_expression()
        if not value:
            raise SyntaxError("Expected expression after 'print'")
        return {
            "type": "print",
            "value": value
        }

    def parse_assignment(self):
        self.consume("ASSIGNMENT")  # Consume 'set'
        if not self.peek() or self.peek()[0] != "IDENTIFIER":
            raise SyntaxError("Expected variable name after 'set'")
        variable = self.consume("IDENTIFIER")
        
        if not self.consume_if_matches("ASSIGNMENT", "to"):
            raise SyntaxError("Expected 'to' after variable name")
            
        value = self.parse_expression()
        if not value:
            raise SyntaxError("Expected expression after 'to'")
            
        return {
            "type": "assignment",
            "variable": variable,
            "value": value
        }

    def parse_expression(self):
        # Try to parse a group creation first
        if self.peek() and self.peek()[0] == "KEYWORD" and self.peek()[1] == "group":
            return self.parse_group_creation()
            
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
        if not self.peek():
            return None
            
        token_type, value = self.peek()
        
        if token_type == "STRING":
            return {
                "type": "string",
                "value": self.consume("STRING")
            }
        elif token_type == "NUMBER":
            return {
                "type": "number",
                "value": self.consume("NUMBER")
            }
        elif token_type == "IDENTIFIER":
            value = self.consume("IDENTIFIER")
            if self.peek() and self.peek()[1] == "(":
                self.position -= 1  # Go back to reparse as function call
                return self.parse_function_call()
            elif self.peek() and self.peek()[1] == "[":
                self.position -= 1  # Go back to reparse as group operation
                return self.parse_group_operation()
            return {
                "type": "identifier",
                "value": value
            }
        elif token_type == "BOOLEAN":
            return {
                "type": "boolean",
                "value": self.consume("BOOLEAN").lower() == "true"
            }
        return None

    def parse_group_creation(self):
        self.consume("KEYWORD")  # Consume 'group'
        
        if not self.peek() or self.peek()[1] != "[":
            raise SyntaxError("Expected '[' after 'group'")
        self.consume("SYMBOL")  # Consume '['
        
        elements = []
        while self.peek() and self.peek()[1] != "]":
            if elements:  # If we already have elements
                if not self.peek() or self.peek()[1] != ",":
                    raise SyntaxError("Expected ',' between group elements")
                self.consume("SYMBOL")  # Consume the comma
            
            element = self.parse_expression()
            if not element:
                raise SyntaxError("Expected expression in group")
            elements.append(element)
        
        if not self.peek() or self.peek()[1] != "]":
            raise SyntaxError("Expected ']' after group elements")
        self.consume("SYMBOL")  # Consume ']'
        
        return {
            "type": "group_creation",
            "elements": elements
        }
    def parse_group_assignment(self):
        """Handle array index assignment statements like 'set arr[0] to 5'"""
        name = self.consume("IDENTIFIER")
        
        if not self.peek() or self.peek()[1] != "[":
            raise SyntaxError("Expected '[' after identifier")
        self.consume("SYMBOL")  # Consume '['
        
        index = self.parse_expression()
        if not index:
            raise SyntaxError("Expected index expression")
        
        if not self.peek() or self.peek()[1] != "]":
            raise SyntaxError("Expected ']' after index")
        self.consume("SYMBOL")  # Consume ']'
        
        if not self.peek() or self.peek()[0] != "ASSIGNMENT" or self.peek()[1] != "to":
            raise SyntaxError("Expected 'to' after array index")
        self.consume("ASSIGNMENT")  # Consume 'to'
        
        value = self.parse_expression()
        if not value:
            raise SyntaxError("Expected expression after 'to'")
        
        return {
            "type": "group_assignment",
            "name": name,
            "index": index,
            "value": value
        }
    
    def parse_if_statement(self):
        """Handle if statements and else blocks."""
        condition = self.parse_expression()
        
        if not self.consume_if_matches("KEYWORD", "then"):
            raise SyntaxError("Expected 'then' after if condition")
            
        then_block = self.parse_block()
        else_block = None
        
        # Check for optional else block
        if self.peek() and self.peek()[0] == "KEYWORD" and self.peek()[1] == "else":
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
        """Handle while loops."""
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

    def parse_group_operation(self):
        name = self.consume("IDENTIFIER")
        self.consume("SYMBOL")  # Consume '['
        
        index = self.parse_expression()
        if not index:
            raise SyntaxError("Expected index expression")
        
        if not self.consume_if_matches("SYMBOL", "]"):
            raise SyntaxError("Expected ']' after index")
        
        # Check if this is an assignment
        if self.peek() and self.peek()[0] == "ASSIGNMENT" and self.peek()[1] == "to":
            self.consume("ASSIGNMENT")  # Consume 'to'
            value = self.parse_expression()
            if not value:
                raise SyntaxError("Expected expression after 'to'")
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

    def parse_block(self):
        statements = []
        while self.peek() and not (self.peek()[0] == "KEYWORD" and 
                                 self.peek()[1] in ["end", "else"]):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements

    def parse_function_definition(self):
        name = self.consume("IDENTIFIER")
        
        if not self.peek() or self.peek()[1] != "(":
            raise SyntaxError("Expected '(' after function name")
        self.consume("SYMBOL")
        
        parameters = []
        while self.peek() and self.peek()[1] != ")":
            if parameters:
                if not self.peek() or self.peek()[1] != ",":
                    raise SyntaxError("Expected ',' between parameters")
                self.consume("SYMBOL")
            
            if not self.peek() or self.peek()[0] != "IDENTIFIER":
                raise SyntaxError("Expected parameter name")
            parameters.append(self.consume("IDENTIFIER"))
        
        if not self.consume_if_matches("SYMBOL", ")"):
            raise SyntaxError("Expected ')' after parameters")
        
        body = self.parse_block()
        
        if not self.consume_if_matches("KEYWORD", "end"):
            raise SyntaxError("Expected 'end' after function body")
            
        self.function_nesting -= 1
        
        return {
            "type": "function_definition",
            "name": name,
            "parameters": parameters,
            "body": body
        }

    def parse_return_statement(self):
        value = self.parse_expression()
        if not value:
            raise SyntaxError("Expected expression after 'return'")
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
                if not self.peek() or self.peek()[1] != ",":
                    raise SyntaxError("Expected ',' between arguments")
                self.consume("SYMBOL")
            
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

    def run(self, text):
        try:
            self.tokens = self.lexer.tokenize(text)
            self.position = 0
            ast = self.parse_statement()
            return ast, None
        except SyntaxError as e:
            return None, str(e)