from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    parser = Parser()
    interpreter = Interpreter()

    while True:
        text = input('>>> ')
        if text.strip().lower() in {"exit", "quit"}:
            print("Exiting SimpleScript.")
            break

        try:

            ast, error = parser.run(text)
            if error:
                print(f"Error: {error}")
            else:
                result = interpreter.evaluate(ast)
                print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")
