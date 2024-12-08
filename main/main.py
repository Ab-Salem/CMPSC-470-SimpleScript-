# main.py
from parser import Parser
from interpreter import Interpreter
import sys

class SimpleScriptRunner:
    def __init__(self):
        self.parser = Parser()
        self.interpreter = Interpreter()

    def execute_file(self, filename):
        try:
            with open(filename, 'r') as file:
                code = file.read()
                # Split the code into lines and execute each line
                lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
                for line_number, line in enumerate(lines, 1):
                    try:
                        ast, error = self.parser.run(line)
                        if error:
                            print(f"Error on line {line_number}: {error}")
                        else:
                            result = self.interpreter.evaluate(ast)
                            if result is not None:
                                print(f"Line {line_number} result: {result}")
                    except Exception as e:
                        print(f"Error executing line {line_number}: {str(e)}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error reading file: {str(e)}")

    def interactive_mode(self):
        print("SimpleScript Interactive Mode (type 'exit' or 'quit' to end)")
        while True:
            try:
                text = input('>>> ')
                if text.strip().lower() in {"exit", "quit"}:
                    print("Exiting SimpleScript.")
                    break

                ast, error = self.parser.run(text)
                if error:
                    print(f"Error: {error}")
                else:
                    result = self.interpreter.evaluate(ast)
                    if result is not None:
                        print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    runner = SimpleScriptRunner()
    if len(sys.argv) > 1:
        # Execute file mode
        runner.execute_file(sys.argv[1])
    else:
        # Interactive mode
        runner.interactive_mode()