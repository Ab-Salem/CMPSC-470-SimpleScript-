# SimpleScript

SimpleScript is a beginner-friendly programming language designed specifically for non-programmers like librarians, teachers, and other professionals who need to automate tasks or solve problems without a technical background. It uses natural, English-like syntax to make programming more accessible and intuitive.

## Why SimpleScript?

- 📝 Uses everyday English words instead of complex programming symbols
- 🎯 Focused on common tasks like data manipulation and file handling
- 🚫 No complicated syntax or technical jargon
- ✨ Clear, readable code that's easy to understand
- 🔄 Simple to learn and remember

## Getting Started

### Installation
1. Make sure you have Python installed on your computer
2. Download the SimpleScript files to your computer
3. Open your terminal or command prompt
4. Navigate to the SimpleScript folder

### Running SimpleScript
You can use SimpleScript in two ways:

1. Interactive Mode (type commands one at a time):
```bash
python main.py
```

2. Run a Script File (execute multiple commands from a file):
```bash
python main.py yourscript.txt
```

## Language Basics

### Variables and Values
Store information using the `set` command:
```
set name to "John"
set age to 25
set greeting to "Hello, " + name
```

### Printing Output
Show information using the `print` command:
```
print "Hello, World!"
print age
print greeting
```

### Basic Math
SimpleScript supports common math operations:
```
set number1 to 10
set number2 to 5

# Addition
print number1 + number2

# Subtraction
print number1 - number2

# Multiplication
print number1 * number2

# Division
print number1 / number2
```

### Comparing Values
Compare values using natural language:
```
set price to 10

if price is less than 20 then
    print "Good deal!"
end
```

### Working with Files
Read and write files easily:
```
# Read from a file
set content to read "myfile.txt"
print content
```

## Example Tasks

### 1. Grade Calculator
```
set score to 85
if score is greater than or equal to 90 then
    print "Grade: A"
else
    if score is greater than or equal to 80 then
        print "Grade: B"
    end
end
```

### 2. Book Inventory
```
set book_title to "The Great Gatsby"
set copies to 5
set status to "Available"

print book_title + " - " + copies + " copies " + status
```

## Language Reference

### Data Types
- Text (Strings): `"Hello"`
- Numbers: `42`, `3.14`
- True/False (Boolean): `true`, `false`

### Operators
Comparison Operators:
- `is equal to`
- `is not equal to`
- `is greater than`
- `is less than`
- `is greater than or equal to`
- `is less than or equal to`

Math Operators:
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Remainder: `%`

### Keywords
- `set`: Create or update variables
- `to`: Used with `set` for assignment
- `print`: Display output
- `if`: Start a condition
- `then`: Use with `if` for conditions
- `else`: Alternative condition
- `end`: End a block of code
- `while`: Create loops
- `function`: Create reusable code
- `and`: Combine conditions
- `or`: Alternative conditions
- `not`: Negate conditions

## Need Help?

- Check our example scripts in the `examples` folder
- Read through the comments in example code
- Try running the code in interactive mode to experiment
- Break down complex tasks into smaller steps

## Contributing
- Abdallah Salem
- Akhil Jobi
- Kamila Anarkulova
- Mahir Sadique
