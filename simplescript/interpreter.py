class Interpreter:
    def __init__(self):
        self.environment = {}  # Dictionary to store variables

    def evaluate(self, node):
        """Evaluate a node in the AST."""
        try:
            node_type = node.get("type")
            if node_type == "assignment":
                return self.evaluate_assignment(node)
            elif node_type == "print":
                return self.evaluate_print(node)
            elif node_type == "binary_operation":
                return self.evaluate_binary_operation(node)
            elif node_type == "number":
                return float(node["value"]) if "." in node["value"] else int(node["value"])
            elif node_type == "string":
                return node["value"]
            elif node_type == "identifier":
                return self.get_variable(node["value"])
            else:
                raise ValueError(f"Unknown node type: {node_type}")
        except KeyError as e:
            raise RuntimeError(f"Invalid AST node structure: Missing key {e}")
        except ZeroDivisionError:
            raise RuntimeError("Division by zero is undefined.")

    def evaluate_assignment(self, node):
        """Handle assignment operations."""
        variable_name = node["variable"]
        value = self.evaluate(node["value"])
        self.environment[variable_name] = value
        return value

    def evaluate_print(self, node):
        """Handle print statements."""
        value = self.evaluate(node["value"])
        print(value)  # Output the value to the console
        return value

    def evaluate_binary_operation(self, node):
        """Handle binary operations."""
        left = self.evaluate(node["left"])
        right = self.evaluate(node["right"])
        operator = node["operator"]

        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero.")
            return left / right
        elif operator == "%":
            return left % right
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def get_variable(self, name):
        """Retrieve a variable's value or raise an error if it's undefined."""
        if name not in self.environment:
            raise RuntimeError(f"Undefined variable: {name}")
        return self.environment[name]
