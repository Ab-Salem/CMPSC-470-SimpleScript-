from parser import Parser
from interpreter import Interpreter
import sys

class SimpleScriptRunner:
    def __init__(self):
        self.parser = Parser()
        self.interpreter = Interpreter()

    def execute_file(self, filename):
        """Execute a SimpleScript file."""
        try:
            with open(filename, 'r') as file:
                code = file.read()
                # Split the code into lines and execute each line
                lines = [line.strip() for line in code.split('\n') 
                        if line.strip() and not line.strip().startswith('#')]
                
                # Track line numbers for error reporting
                current_line = 0
                try:
                    while current_line < len(lines):
                        line = lines[current_line]
                        
                        # Handle multi-line statements (function definitions, if statements, while loops)
                        if any(line.startswith(keyword) for keyword in ['function', 'if', 'while']):
                            block_lines = [line]
                            nesting_level = 1
                            current_line += 1
                            
                            # Collect all lines in the block
                            while current_line < len(lines) and nesting_level > 0:
                                line = lines[current_line]
                                if any(line.startswith(keyword) for keyword in ['function', 'if', 'while']):
                                    nesting_level += 1
                                elif line == 'end':
                                    nesting_level -= 1
                                block_lines.append(line)
                                current_line += 1
                            
                            # Join the block lines and execute as one unit
                            block_code = ' '.join(block_lines)
                            self.execute_line(block_code, current_line - len(block_lines) + 1)
                        else:
                            # Execute single-line statement
                            self.execute_line(line, current_line + 1)
                            current_line += 1
                            
                except Exception as e:
                    print(f"Error on line {current_line + 1}: {str(e)}")
                    
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error reading file: {str(e)}")

    def execute_line(self, line, line_number):
        """Execute a single line or block of SimpleScript code."""
        try:
            ast, error = self.parser.run(line)
            if error:
                print(f"Error on line {line_number}: {error}")
            else:
                result = self.interpreter.evaluate(ast)
                # Only print results for expressions that aren't handled by print statements
                if result is not None and not (isinstance(ast, dict) and ast.get('type') == 'print'):
                    print(f"Line {line_number} result: {result}")
        except Exception as e:
            raise RuntimeError(f"Error executing line {line_number}: {str(e)}")

    def interactive_mode(self):
        """Run SimpleScript in interactive mode."""
        print("SimpleScript Interactive Mode (type 'exit' or 'quit' to end)")
        print("Type 'help' for a list of commands and examples")
        
        while True:
            try:
                text = input('>>> ')
                if text.strip().lower() in {"exit", "quit"}:
                    print("Exiting SimpleScript.")
                    break
                elif text.strip().lower() == "help":
                    self.show_help()
                    continue
                
                # Handle multi-line input for blocks
                if any(text.startswith(keyword) for keyword in ['function', 'if', 'while']):
                    block_text = [text]
                    nesting_level = 1
                    
                    # Keep reading lines until the block is complete
                    while nesting_level > 0:
                        line = input('... ')
                        if any(line.startswith(keyword) for keyword in ['function', 'if', 'while']):
                            nesting_level += 1
                        elif line == 'end':
                            nesting_level -= 1
                        block_text.append(line)
                    
                    text = ' '.join(block_text)
                
                ast, error = self.parser.run(text)
                if error:
                    print(f"Error: {error}")
                else:
                    result = self.interpreter.evaluate(ast)
                    # Only print results for expressions that aren't handled by print statements
                    if result is not None and not (isinstance(ast, dict) and ast.get('type') == 'print'):
                        print(f"Result: {result}")
                        
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to exit SimpleScript.")
            except Exception as e:
                print(f"Error: {str(e)}")

    def show_help(self):
        """Display help information and examples."""
        help_text = """
SimpleScript Commands and Examples:

Variables and Basic Operations:
    set x to 42
    set name to "John"
    print x + 5
    print "Hello, " + name

Groups (Arrays):
    set numbers to group [1, 2, 3, 4, 5]
    print numbers[0]
    set numbers[1] to 10

User Input:
    set name to ask "What's your name? "
    print "Hello, " + name

Control Flow:
    if x is greater than 0 then
        print "Positive"
    else
        print "Non-positive"
    end

    while counter is less than 5 do
        print counter
        set counter to counter + 1
    end

Functions:
    function greet(name)
        print "Hello, " + name
        return "Greeting completed"
    end

    function factorial(n)
        if n is less than or equal to 1 then
            return 1
        else
            return n * factorial(n - 1)
        end
    end

File Operations:
    read "filename.txt"

Comparison Operators:
    is equal to
    is not equal to
    is greater than
    is less than
    is greater than or equal to
    is less than or equal to

Logical Operators:
    and
    or
    not

Type 'exit' or 'quit' to end the session
"""
        print(help_text)

if __name__ == "__main__":
    runner = SimpleScriptRunner()
    if len(sys.argv) > 1:
        # Execute file mode
        runner.execute_file(sys.argv[1])
    else:
        # Interactive mode
        runner.interactive_mode()