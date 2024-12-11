from file_handler import FileHandler

class Interpreter:
    def __init__(self):
        self.environment = {}
        self.functions = {}
        self.file_handler = FileHandler(self)
        self.return_value = None

    def evaluate(self, node):
        """Main evaluation method."""
        try:
            node_type = node.get("type")
            
            if node_type == "number":
                return float(node["value"]) if "." in str(node["value"]) else int(node["value"])
            elif node_type == "string":
                return node["value"].strip('"')
            elif node_type == "boolean":
                return node["value"]
            elif node_type == "identifier":
                return self.get_variable(node["value"])
            elif node_type == "binary_operation":
                return self.evaluate_binary_operation(node)
            elif node_type == "logical_operation":
                return self.evaluate_logical_operation(node)
            elif node_type == "comparison_operation":
                return self.evaluate_comparison_operation(node)
            elif node_type == "assignment":
                return self.evaluate_assignment(node)
            elif node_type == "print":
                return self.evaluate_print(node)
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
            else:
                raise RuntimeError(f"Unknown node type: {node_type}")
        except Exception as e:
            raise RuntimeError(str(e))

    def evaluate_in_env(self, node, env):
        """Evaluate an expression in a specific environment."""
        old_env = self.environment
        try:
            self.environment = env
            return self.evaluate(node)
        finally:
            self.environment = old_env

    def evaluate_assignment(self, node):
        """Handle variable assignment."""
        value = self.evaluate(node["value"])
        self.environment[node["variable"]] = value
        return value

    def evaluate_print(self, node):
        """Handle print statements."""
        value = self.evaluate(node["value"])
        print(value)
        return value

    def evaluate_binary_operation(self, node):
        """Handle binary operations (+, -, *, /, %)."""
        left = self.evaluate(node["left"])
        right = self.evaluate(node["right"])
        op = node["operator"]
        
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif op == "%":
            if right == 0:
                raise RuntimeError("Modulo by zero")
            return left % right
        else:
            raise RuntimeError(f"Unknown operator: {op}")

    def evaluate_logical_operation(self, node):
        """Handle logical operations (and, or, not)."""
        operator = node["operator"]
        
        if operator == "not":
            return not self.evaluate(node["right"])
            
        left = self.evaluate(node["left"])
        right = self.evaluate(node["right"])
        
        operations = {
            "and": lambda x, y: x and y,
            "or": lambda x, y: x or y
        }
        
        if operator not in operations:
            raise RuntimeError(f"Unknown logical operator: {operator}")
            
        return operations[operator](left, right)

    def evaluate_comparison_operation(self, node):
        """Handle comparison operations."""
        left = self.evaluate(node["left"])
        right = self.evaluate(node["right"])
        op = node["operator"]
        
        operations = {
            "is equal to": lambda x, y: x == y,
            "is not equal to": lambda x, y: x != y,
            "is less than": lambda x, y: x < y,
            "is greater than": lambda x, y: x > y,
            "is less than or equal to": lambda x, y: x <= y,
            "is greater than or equal to": lambda x, y: x >= y
        }
        
        if op not in operations:
            raise RuntimeError(f"Unknown comparison operator: {op}")
            
        return operations[op](left, right)

    def evaluate_if_statement(self, node):
        """Handle if statements."""
        condition = self.evaluate(node["condition"])
        if condition:
            return self.evaluate_block(node["then_block"])
        elif node.get("else_block"):
            return self.evaluate_block(node["else_block"])
        return None

    def evaluate_while_statement(self, node):
        """Handle while loops."""
        result = None
        saved_return_value = self.return_value  # Save any existing return value
        self.return_value = None  # Reset return value for loop execution
        
        try:
            while self.evaluate(node["condition"]):
                for statement in node["body"]:
                    result = self.evaluate(statement)
                    # Only exit loop if we're in a function and got a return
                    if self.return_value is not None and self.in_function:
                        return result
        finally:
            # Restore the previous return value
            self.return_value = saved_return_value
        
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
        func_name = node["name"]
        if func_name not in self.functions:
            raise RuntimeError(f"Undefined function: {func_name}")
                
        func = self.functions[func_name]
        if len(node["arguments"]) != len(func["parameters"]):
            raise RuntimeError(f"Expected {len(func['parameters'])} arguments, got {len(node['arguments'])}")
                
        # Save current environment and return value
        outer_env = self.environment.copy()
        saved_return_value = self.return_value
        self.return_value = None  # Reset return value for function execution
        
        try:
            # Create new environment for function execution
            self.environment = {}
            self.in_function = True  # Mark that we're in a function
            
            # Evaluate arguments and bind to parameters
            for param, arg in zip(func["parameters"], node["arguments"]):
                arg_value = self.evaluate_in_env(arg, outer_env)
                self.environment[param] = arg_value
            
            # Execute function body
            result = None
            for stmt in func["body"]:
                result = self.evaluate(stmt)
                if self.return_value is not None:
                    break
            
            return self.return_value if self.return_value is not None else result
                
        finally:
            # Restore outer environment and previous return value
            self.environment = outer_env
            self.in_function = False
            if not self.in_function:  # Only reset return value if we're not in a nested function
                self.return_value = saved_return_value

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