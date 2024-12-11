# lexer.py
import re

class Lexer:
    def __init__(self):
        self.keywords = {
            "set", "to", "print", "ask", "and", "store", "if", "then", "else",
            "while", "do", "repeat", "function", "output", "end", "read", 
            "true", "false", "return", "group"
        }
        self.token_patterns = [
            # First match keywords and compound operators
            (r'\b(function|if|then|else|while|do|end|return|group|ask)\b', "KEYWORD"),
            (r'\b(is equal to|is not equal to|is greater than or equal to|is less than or equal to|is greater than|is less than)\b', "COMPARISON"),
            (r'\b(and|or|not)\b', "LOGICAL"),
            (r'\b(true|false)\b', "BOOLEAN"),
            (r'\b(set|to|read)\b', "ASSIGNMENT"),
            # Then match literals and symbols
            (r'\b\d+(\.\d+)?\b', "NUMBER"),
            (r'"[^"]*"', "STRING"),
            (r'[+\-*/%]', "ARITHMETIC"),
            (r'[\(\)\[\],]', "SYMBOL"),  # Separated symbols for better matching
            # Match identifiers last to avoid keyword conflicts
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', "IDENTIFIER"),
            (r'\s+', None),  # Skip whitespace
        ]

    def tokenize(self, code):
        tokens = []
        position = 0
        while position < len(code):
            match = None
            for pattern, token_type in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(code, position)
                if match:
                    if token_type:
                        value = match.group(0)
                        tokens.append((token_type, value))
                    position = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {code[position]}")
        return tokens