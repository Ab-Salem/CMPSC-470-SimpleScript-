# file_handler.py
class FileHandler:
    def __init__(self, interpreter):
        self.interpreter = interpreter
    
    def read_file(self, filename):
        """Read contents from a file."""
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise RuntimeError(f"File not found: {filename}")
        except IOError as e:
            raise RuntimeError(f"Error reading file: {str(e)}")