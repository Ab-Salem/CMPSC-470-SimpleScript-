import re

class Lexer:
    def __init__(self):
        self.keywords = {
            "set", "to", "print", "ask", "and", "store", "if", "then", "else",
            "while", "do", "repeat", "function", "output", "end"
        }
        self.token_patterns = [
            (r'\b\d+(\.\d+)?\b', "NUMBER"),  # Number
            (r'"[^"]*"', "STRING"),          # String
            (r'\b(is equal to|is not equal to|is greater than|is less than|is greater than or equal to|is less than or equal to)\b', "COMPARISON"),
            (r'\b(and|or|not)\b', "LOGICAL"),
            (r'\b(set|to)\b', "ASSIGNMENT"),
            (r'[+\-*/%]', "ARITHMETIC"),
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', "IDENTIFIER"),  # Variable names
            (r'[{}()\[\],]', "SYMBOL"),      # Symbols
            (r'\s+', None),                  # Skip whitespace
        ]

    def tokenize(self, code):
        tokens = []  # Start fresh for each input
        position = 0
        while position < len(code):
            match = None
            for pattern, token_type in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(code, position)
                if match:
                    if token_type:  # Skip tokens with None type
                        value = match.group(0)
                        tokens.append((token_type, value))
                    position = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {code[position]}")
        return tokens
