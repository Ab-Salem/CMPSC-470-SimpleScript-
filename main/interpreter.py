from file_handler import FileHandler

# interpreter.py (continued)
class Interpreter:
    def __init__(self):
        self.environment = {}
        self.functions = {}
        self.file_handler = FileHandler(self)
        self.return_value = None

    def evaluate(self, node):
        try:
            node_type = node.get("type")
            if node_type == "assignment":
                return self.evaluate_assignment(node)
            elif node_type == "print":
                return self.evaluate_print(node)
            elif node_type == "binary_operation":
                return self.evaluate_binary_operation(node)
            elif node_type == "logical_operation":
                return self.evaluate_logical_operation(node)
            elif node_type == "comparison_operation":
                return self.evaluate_comparison_operation(node)
            elif node_type == "if_statement":
                return self.evaluate_if_statement(node)
            elif node_type == "while_statement":
                return self.evaluate_while_statement(node)
            elif node_type == "function_definition":
                return self.evaluate_function_definition(node)
            elif node_type == "function_call":
                return self.evaluate_function_call(node)
            elif node_type == "return_statement":
                return self.evaluate_return_statement(node)
            elif node_type == "read_file":
                return self.evaluate_read_file(node)
            elif node_type == "ask":
                return self.evaluate_ask(node)
            elif node_type == "group_creation":
                return self.evaluate_group_creation(node)
            elif node_type == "group_access":
                return self.evaluate_group_access(node)
            elif node_type == "group_assignment":
                return self.evaluate_group_assignment(node)
            elif node_type == "number":
                return float(node["value"]) if "." in str(node["value"]) else int(node["value"])
            elif node_type == "string":
                return node["value"].strip('"')
            elif node_type == "boolean":
                return node["value"]
            elif node_type == "identifier":
                return self.get_variable(node["value"])
            else:
                raise ValueError(f"Unknown node type: {node_type}")
        except KeyError as e:
            raise RuntimeError(f"Invalid AST node structure: Missing key {e}")

    def evaluate_assignment(self, node):
        """Handle assignment operations."""
        variable_name = node["variable"]
        value = self.evaluate(node["value"])
        self.environment[variable_name] = value
        return value

    def evaluate_print(self, node):
        """Handle print statements."""
        value = self.evaluate(node["value"])
        print(value)
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
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif operator == "%":
            return left % right
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def evaluate_logical_operation(self, node):
        """Handle logical operations (and, or, not)."""
        operator = node["operator"]
        if operator == "not":
            value = self.evaluate(node["right"])
            return not value
            
        left = self.evaluate(node["left"])
        right = self.evaluate(node["right"])
        
        if operator == "and":
            return left and right
        elif operator == "or":
            return left or right
        else:
            raise ValueError(f"Unknown logical operator: {operator}")

    def evaluate_comparison_operation(self, node):
        """Handle comparison operations."""
        left = self.evaluate(node["left"])
        right = self.evaluate(node["right"])
        operator = node["operator"]
        
        comparison_ops = {
            "is equal to": lambda x, y: x == y,
            "is not equal to": lambda x, y: x != y,
            "is greater than": lambda x, y: x > y,
            "is less than": lambda x, y: x < y,
            "is greater than or equal to": lambda x, y: x >= y,
            "is less than or equal to": lambda x, y: x <= y
        }
        
        if operator not in comparison_ops:
            raise ValueError(f"Unknown comparison operator: {operator}")
            
        return comparison_ops[operator](left, right)

    def evaluate_if_statement(self, node):
        """Handle if statements."""
        condition = self.evaluate(node["condition"])
        if condition:
            return self.evaluate_block(node["then_block"])
        elif node["else_block"]:
            return self.evaluate_block(node["else_block"])
        return None

    def evaluate_while_statement(self, node):
        """Handle while loops."""
        result = None
        while self.evaluate(node["condition"]):
            result = self.evaluate_block(node["body"])
            if self.return_value is not None:
                break
        return result

    def evaluate_function_definition(self, node):
        """Handle function definitions."""
        self.functions[node["name"]] = {
            "parameters": node["parameters"],
            "body": node["body"]
        }
        return None

    def evaluate_function_call(self, node):
        """Handle function calls."""
        if node["name"] not in self.functions:
            raise RuntimeError(f"Undefined function: {node['name']}")
            
        func = self.functions[node["name"]]
        if len(node["arguments"]) != len(func["parameters"]):
            raise RuntimeError(f"Expected {len(func['parameters'])} arguments, got {len(node['arguments'])}")
            
        # Create new scope for function
        old_env = self.environment.copy()
        self.environment = {}
        
        # Evaluate arguments and bind to parameters
        for param, arg in zip(func["parameters"], node["arguments"]):
            self.environment[param] = self.evaluate(arg)
            
        # Execute function body
        self.return_value = None
        result = self.evaluate_block(func["body"])
        
        # Restore old scope
        self.environment = old_env
        
        # Return the function's return value or last statement result
        return self.return_value if self.return_value is not None else result

    def evaluate_return_statement(self, node):
        """Handle return statements."""
        self.return_value = self.evaluate(node["value"])
        return self.return_value

    def evaluate_read_file(self, node):
        """Handle file reading operations."""
        filename = self.evaluate(node["filename"])
        if not isinstance(filename, str):
            raise RuntimeError("Filename must be a string")
        return self.file_handler.read_file(filename)

    def evaluate_ask(self, node):
        """Handle input operations."""
        prompt = self.evaluate(node["prompt"])
        return input(str(prompt))

    def evaluate_group_creation(self, node):
        """Handle group (array) creation."""
        return [self.evaluate(element) for element in node["elements"]]

    def evaluate_group_access(self, node):
        """Handle group element access."""
        group = self.get_variable(node["name"])
        if not isinstance(group, list):
            raise RuntimeError(f"Variable '{node['name']}' is not a group")
            
        index = self.evaluate(node["index"])
        if not isinstance(index, int):
            raise RuntimeError("Group index must be an integer")
            
        if index < 0 or index >= len(group):
            raise RuntimeError(f"Group index {index} out of range")
            
        return group[index]

    def evaluate_group_assignment(self, node):
        """Handle group element assignment."""
        group = self.get_variable(node["name"])
        if not isinstance(group, list):
            raise RuntimeError(f"Variable '{node['name']}' is not a group")
            
        index = self.evaluate(node["index"])
        if not isinstance(index, int):
            raise RuntimeError("Group index must be an integer")
            
        if index < 0 or index >= len(group):
            raise RuntimeError(f"Group index {index} out of range")
            
        value = self.evaluate(node["value"])
        group[index] = value
        return value

    def evaluate_block(self, statements):
        """Evaluate a block of statements."""
        result = None
        for stmt in statements:
            result = self.evaluate(stmt)
            if self.return_value is not None:
                break
        return result

    def get_variable(self, name):
        """Retrieve a variable's value."""
        if name not in self.environment:
            raise RuntimeError(f"Undefined variable: {name}")
        return self.environment[name]