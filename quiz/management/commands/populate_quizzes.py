from django.core.management.base import BaseCommand
from quiz.models import Quiz, Question, Option

class Command(BaseCommand):
    help = 'Populate database with predefined quizzes'

    def handle(self, *args, **kwargs):
        # Web Programming Quiz
        web_quiz = Quiz.objects.create(
            title='Web Programming Basics',
            description='Explore the essential concepts of web development, including HTML, CSS, and JavaScript, and test your knowledge with this engaging quiz.',
            duration=30
        )

        web_questions = [
            {
                'text': 'Which of the following is NOT a web browser?',
                'options': [
                    ('A. Chrome', False),
                    ('B. Firefox', False),
                    ('C. Edge', False),
                    ('D. Python', True)
                ]
            },
            {
                'text': 'What does HTTP stand for?',
                'options': [
                    ('A. HyperText Transmission Protocol', False),
                    ('B. HyperText Transfer Protocol', True),
                    ('C. HighText Transfer Protocol', False),
                    ('D. HyperText Transfer Packet', False)
                ]
            },
            {
                'text': 'What is the correct HTML element for the largest heading?',
                'options': [
                    ('A. <h1>', True),
                    ('B. <h6>', False),
                    ('C. <header>', False),
                    ('D. <h0>', False)
                ]
            },
            {
                'text': 'Which HTML attribute is used to define inline styles?',
                'options': [
                    ('A. class', False),
                    ('B. style', True),
                    ('C. id', False),
                    ('D. css', False)
                ]
            },
            {
                'text': 'Which property is used in CSS to change text color?',
                'options': [
                    ('A. color', True),
                    ('B. font-color', False),
                    ('C. text-color', False),
                    ('D. background-color', False)
                ]
            },
            {
                'text': 'What does the "C" in CSS stand for?',
                'options': [
                    ('A. Complex', False),
                    ('B. Cascading', True),
                    ('C. Creative', False),
                    ('D. Custom', False)
                ]
            },
            {
                'text': 'Which tag is used for adding a line break in HTML?',
                'options': [
                    ('A. <break>', False),
                    ('B. <lb>', False),
                    ('C. <br>', True),
                    ('D. <line>', False)
                ]
            },
            {
                'text': 'What does <ul> represent in HTML?',
                'options': [
                    ('A. Underline', False),
                    ('B. Unordered List', True),
                    ('C. Uniform Layout', False),
                    ('D. User List', False)
                ]
            },
            {
                'text': 'What is the default method for submitting forms in HTML?',
                'options': [
                    ('A. GET', True),
                    ('B. POST', False),
                    ('C. PUT', False),
                    ('D. DELETE', False)
                ]
            },
            {
                'text': 'Which of the following is NOT a JavaScript framework?',
                'options': [
                    ('A. Angular', False),
                    ('B. React', False),
                    ('C. Django', True),
                    ('D. Vue', False)
                ]
            },
            {
                'text': 'In CSS, what does z-index control?',
                'options': [
                    ('A. The zoom level', False),
                    ('B. The stacking order of elements', True),
                    ('C. The size of the element', False),
                    ('D. The background image', False)
                ]
            },
            {
                'text': 'What is the purpose of the <meta> tag in HTML?',
                'options': [
                    ('A. Adding links to external stylesheets', False),
                    ('B. Storing metadata about the webpage', True),
                    ('C. Inserting media elements', False),
                    ('D. Embedding JavaScript', False)
                ]
            },
            {
                'text': 'What is Bootstrap used for?',
                'options': [
                    ('A. Database management', False),
                    ('B. Front-end framework for responsive design', True),
                    ('C. Back-end server handling', False),
                    ('D. Debugging JavaScript', False)
                ]
            },
            {
                'text': 'What does <iframe> do in HTML?',
                'options': [
                    ('A. Embeds a video', False),
                    ('B. Embeds another HTML page', True),
                    ('C. Creates a pop-up window', False),
                    ('D. Creates a scrollable region', False)
                ]
            },
            {
                'text': 'Which CSS property is used to make text bold?',
                'options': [
                    ('A. weight', False),
                    ('B. font-weight', True),
                    ('C. bold', False),
                    ('D. text-style', False)
                ]
            },
            {
                'text': 'What is a favicon?',
                'options': [
                    ('A. A small image displayed in the browser tab', True),
                    ('B. A type of button', False),
                    ('C. An external link', False),
                    ('D. A navigation icon', False)
                ]
            },
            {
                'text': 'What does the <title> tag do?',
                'options': [
                    ('A. Displays text in the header', False),
                    ('B. Sets the title of the document in the browser tab', True),
                    ('C. Creates a heading', False),
                    ('D. Sets metadata', False)
                ]
            },
            {
                'text': 'Which tag is used to insert an image in HTML?',
                'options': [
                    ('A. <img>', True),
                    ('B. <image>', False),
                    ('C. <pic>', False),
                    ('D. <media>', False)
                ]
            },
            {
                'text': 'What is the primary purpose of the <nav> element in HTML?',
                'options': [
                    ('A. To include navigation links', True),
                    ('B. To display images', False),
                    ('C. To embed videos', False),
                    ('D. To create lists', False)
                ]
            },
            {
                'text': 'What is the correct syntax for linking an external CSS file?',
                'options': [
                    ('A. <link rel="stylesheet" href="style.css">', True),
                    ('B. <style href="style.css">', False),
                    ('C. <css src="style.css">', False),
                    ('D. <stylesheet link="style.css">', False)
                ]
            },
        ]

        self._create_questions(web_quiz, web_questions)

        # Database Quiz
        db_quiz = Quiz.objects.create(
            title='Database Basics',
            description='Explore the fundamental concepts of databases, including relational models, SQL commands, and data integrity, and test your knowledge with this engaging quiz.',
            duration=30
        )

        db_questions = [
            {
                'text': 'What does a relational database store data in?',
                'options': [
                    ('A) Arrays', False),
                    ('B) Tables', True),
                    ('C) Graphs', False),
                    ('D) Files', False)
                ]
            },
            {
                'text': 'What does DDL stand for in SQL?',
                'options': [
                    ('A) Data Description Language', False),
                    ('B) Data Definition Language', True),
                    ('C) Database Design Language', False),
                    ('D) Data Deployment Language', False)
                ]
            },
            {
                'text': 'Which SQL command is used to remove all records from a table?',
                'options': [
                    ('A) DELETE', False),
                    ('B) DROP', False),
                    ('C) CLEAR', False),
                    ('D) TRUNCATE', True)
                ]
            },
            {
                'text': 'What is a database index used for?',
                'options': [
                    ('A) Sorting data', False),
                    ('B) Increasing retrieval speed', True),
                    ('C) Adding constraints', False),
                    ('D) Storing temporary data', False)
                ]
            },
            {
                'text': 'Which of the following is NOT a type of database?',
                'options': [
                    ('A) Hierarchical', False),
                    ('B) Relational', False),
                    ('C) Network', False),
                    ('D) Sequential', True)
                ]
            },
            {
                'text': 'What is a database schema?',
                'options': [
                    ('A) The data stored in a table', False),
                    ('B) A visual representation of data', False),
                    ('C) The structure that defines a database', True),
                    ('D) A backup of a database', False)
                ]
            },
            {
                'text': 'What does ACID stand for in databases?',
                'options': [
                    ('A) Atomicity, Consistency, Isolation, Durability', True),
                    ('B) Accuracy, Consistency, Integrity, Dependability', False),
                    ('C) Access, Control, Integration, Durability', False),
                    ('D) Atomicity, Control, Isolation, Dependency', False)
                ]
            },
            {
                'text': 'Which SQL clause is used to filter records?',
                'options': [
                    ('A) WHERE', True),
                    ('B) FILTER', False),
                    ('C) SEARCH', False),
                    ('D) FIND', False)
                ]
            },
            {
                'text': 'What is the function of a foreign key?',
                'options': [
                    ('A) Link two tables', True),
                    ('B) Encrypt data', False),
                    ('C) Sort records', False),
                    ('D) Add uniqueness to a column', False)
                ]
            },
            {
                'text': 'What is a NULL value in a database?',
                'options': [
                    ('A) A default value', False),
                    ('B) A missing or undefined value', True),
                    ('C) A zero value', False),
                    ('D) A deleted record', False)
                ]
            },
            {
                'text': 'Which SQL keyword is used to sort results?',
                'options': [
                    ('A) ORDER BY', True),
                    ('B) SORT BY', False),
                    ('C) GROUP BY', False),
                    ('D) ARRANGE', False)
                ]
            },
            {
                'text': 'What is a view in a database?',
                'options': [
                    ('A) A temporary table', False),
                    ('B) A virtual table based on SQL query results', True),
                    ('C) A stored procedure', False),
                    ('D) A graphical representation of a table', False)
                ]
            },
            {
                'text': 'Which of the following is a NoSQL database?',
                'options': [
                    ('A) MySQL', False),
                    ('B) MongoDB', True),
                    ('C) PostgreSQL', False),
                    ('D) SQLite', False)
                ]
            },
            {
                'text': 'What is the purpose of normalization in databases?',
                'options': [
                    ('A) Reduce redundancy and improve data integrity', True),
                    ('B) Increase storage space', False),
                    ('C) Add more tables', False),
                    ('D) Increase retrieval speed', False)
                ]
            },
            {
                'text': 'What does a JOIN clause do in SQL?',
                'options': [
                    ('A) Deletes data', False),
                    ('B) Combines rows from two or more tables', True),
                    ('C) Updates records', False),
                    ('D) Creates a new table', False)
                ]
            },
            {
                'text': 'What is a stored procedure?',
                'options': [
                    ('A) A predefined SQL function stored in the database', True),
                    ('B) A temporary table', False),
                    ('C) A database schema', False),
                    ('D) A unique key', False)
                ]
            },
            {
                'text': 'What is the function of the SQL GROUP BY clause?',
                'options': [
                    ('A) Filter rows', False),
                    ('B) Aggregate data into groups', True),
                    ('C) Sort records', False),
                    ('D) Create new tables', False)
                ]
            },
            {
                'text': 'What does the DISTINCT keyword do in SQL?',
                'options': [
                    ('A) Removes duplicate records', True),
                    ('B) Adds a unique constraint', False),
                    ('C) Defines a primary key', False),
                    ('D) Deletes records', False)
                ]
            },
            {
                'text': 'What is a database transaction?',
                'options': [
                    ('A) A single unit of work in a database', True),
                    ('B) A backup process', False),
                    ('C) A query to retrieve data', False),
                    ('D) An SQL command for creating tables', False)
                ]
            },
            {
                'text': 'Which of these is a database constraint?',
                'options': [
                    ('A) PRIMARY KEY', False),
                    ('B) FOREIGN KEY', False),
                    ('C) UNIQUE', False),
                    ('D) All of the above', True)
                ]
            },
        ]

        self._create_questions(db_quiz, db_questions)

        # Python Quiz
        python_quiz = Quiz.objects.create(
            title='Python Basics',
            description='Dive into the essential concepts of Python programming, including data types, control structures, functions, and object-oriented programming, and test your knowledge with this engaging quiz.',
            duration=30
        )

        python_questions = [
            {
                'text': 'What is the correct file extension for Python files?',
                'options': [
                    ('A) .py', True),
                    ('B) .pt', False),
                    ('C) .python', False),
                    ('D) .pyt', False)
                ]
            },
            {
                'text': 'Which function is used to display output in Python?',
                'options': [
                    ('A) echo()', False),
                    ('B) display()', False),
                    ('C) print()', True),
                    ('D) show()', False)
                ]
            },
            {
                'text': 'What is the result of 3 ** 2 in Python?',
                'options': [
                    ('A) 5', False),
                    ('B) 6', False),
                    ('C) 9', True),
                    ('D) 8', False)
                ]
            },
            {
                'text': 'Which of the following is a Python data type?',
                'options': [
                    ('A) String', False),
                    ('B) List', False),
                    ('C) Dictionary', False),
                    ('D) All of the above', True)
                ]
            },
            {
                'text': 'How do you start a comment in Python?',
                'options': [
                    ('A) //', False),
                    ('B) /*', False),
                    ('C) #', True),
                    ('D) <!--', False)
                ]
            },
            {
                'text': 'What is the output of len("Hello")?',
                'options': [
                    ('A) 4', False),
                    ('B) 5', True),
                    ('C) 6', False),
                    ('D) Error', False)
                ]
            },
            {
                'text': 'What is the purpose of the input() function?',
                'options': [
                    ('A) Display output', False),
                    ('B) Accept user input', True),
                    ('C) Terminate the program', False),
                    ('D) Repeat a process', False)
                ]
            },
            {
                'text': 'What is the correct way to create a list in Python?',
                'options': [
                    ('A) {1, 2, 3}', False),
                    ('B) [1, 2, 3]', True),
                    ('C) (1, 2, 3)', False),
                    ('D) <1, 2, 3>', False)
                ]
            },
            {
                'text': 'What is the output of 5 // 2?',
                'options': [
                    ('A) 2', True),
                    ('B) 2.5', False),
                    ('C) 3', False),
                    ('D) Error', False)
                ]
            },
            {
                'text': 'How do you define a function in Python?',
                'options': [
                    ('A) function myFunc()', False),
                    ('B) def myFunc():', True),
                    ('C) func myFunc()', False),
                    ('D) myFunc():', False)
                ]
            },
            {
                'text': 'Which keyword is used to create a class in Python?',
                'options': [
                    ('A) define', False),
                    ('B) func', False),
                    ('C) class', True),
                    ('D) object', False)
                ]
            },
            {
                'text': 'What is a tuple in Python?',
                'options': [
                    ('A) A mutable sequence', False),
                    ('B) An immutable sequence', True),
                    ('C) A function', False),
                    ('D) A string', False)
                ]
            },
            {
                'text': 'What is the output of bool(0) in Python?',
                'options': [
                    ('A) True', False),
                    ('B) False', True),
                    ('C) None', False),
                    ('D) Error', False)
                ]
            },
            {
                'text': 'What does break do in a loop?',
                'options': [
                    ('A) Skips the current iteration', False),
                    ('B) Exits the loop', True),
                    ('C) Restarts the loop', False),
                    ('D) Ends the program', False)
                ]
            },
            {
                'text': 'Which keyword is used to handle exceptions in Python?',
                'options': [
                    ('A) catch', False),
                    ('B) except', True),
                    ('C) error', False),
                    ('D) trycatch', False)
                ]
            },
            {
                'text': 'What is the correct way to import a module in Python?',
                'options': [
                    ('A) import module_name', True),
                    ('B) use module_name', False),
                    ('C) include module_name', False),
                    ('D) require module_name', False)
                ]
            },
            {
                'text': 'What does None represent in Python?',
                'options': [
                    ('A) A number', False),
                    ('B) A string', False),
                    ('C) A null value', True),
                    ('D) An error', False)
                ]
            },
            {
                'text': 'How do you access the first element of a list my_list?',
                'options': [
                    ('A) my_list[0]', True),
                    ('B) my_list[1]', False),
                    ('C) my_list[-1]', False),
                    ('D) my_list.first()', False)
                ]
            },
            {
                'text': 'What is the purpose of the range() function?',
                'options': [
                    ('A) Create strings', False),
                    ('B) Iterate over numbers', True),
                    ('C) Generate random numbers', False),
                    ('D) Sort lists', False)
                ]
            },
            {
                'text': 'Which of these is used to create a block of code in Python?',
                'options': [
                    ('A) Parentheses', False),
                    ('B) Curly braces', False),
                    ('C) Indentation', True),
                    ('D) Square brackets', False)
                ]
            },
        ]

        self._create_questions(python_quiz, python_questions)

        # JavaScript Quiz
        js_quiz = Quiz.objects.create(
            title='JavaScript Basics',
            description='Explore the fundamental concepts of JavaScript programming, including syntax, data types, functions, and event handling, and test your knowledge with this engaging quiz.',
            duration=30
        )

        js_questions = [
            {
                'text': 'What is the correct syntax to output "Hello, World!" in JavaScript?',
                'options': [
                    ('A) console.log("Hello, World!");', True),
                    ('B) echo "Hello, World!";', False),
                    ('C) print("Hello, World!");', False),
                    ('D) write("Hello, World!");', False)
                ]
            },
            {
                'text': 'Which keyword is used to declare a variable in JavaScript?',
                'options': [
                    ('A) var', False),
                    ('B) let', False),
                    ('C) const', False),
                    ('D) All of the above', True)
                ]
            },
            {
                'text': 'What does typeof operator do in JavaScript?',
                'options': [
                    ('A) Defines a variable\'s type', False),
                    ('B) Returns the data type of a variable', True),
                    ('C) Converts data types', False),
                    ('D) Checks for errors', False)
                ]
            },
            {
                'text': 'What is the value of NaN in JavaScript?',
                'options': [
                    ('A) null', False),
                    ('B) undefined', False),
                    ('C) Not a Number', True),
                    ('D) Zero', False)
                ]
            },
            {
                'text': 'How do you write a comment in JavaScript?',
                'options': [
                    ('A) // This is a comment', True),
                    ('B) <!-- This is a comment -->', False),
                    ('C) # This is a comment', False),
                    ('D) /* This is a comment */', False)
                ]
            },
            {
                'text': 'Which method is used to round a number to the nearest integer?',
                'options': [
                    ('A) Math.ceil()', False),
                    ('B) Math.floor()', False),
                    ('C) Math.round()', True),
                    ('D) Math.random()', False)
                ]
            },
            {
                'text': 'How do you declare an array in JavaScript?',
                'options': [
                    ('A) {1, 2, 3}', False),
                    ('B) [1, 2, 3]', True),
                    ('C) (1, 2, 3)', False),
                    ('D) <1, 2, 3>', False)
                ]
            },
            {
                'text': 'What is the default value of an uninitialized variable in JavaScript?',
                'options': [
                    ('A) null', False),
                    ('B) undefined', True),
                    ('C) 0', False),
                    ('D) false', False)
                ]
            },
            {
                'text': 'How do you add a new element to the end of an array?',
                'options': [
                    ('A) array.add()', False),
                    ('B) array.push()', True),
                    ('C) array.append()', False),
                    ('D) array.insert()', False)
                ]
            },
            {
                'text': 'What is the purpose of JSON.stringify()?',
                'options': [
                    ('A) Convert an object into a string', True),
                    ('B) Parse a string into an object', False),
                    ('C) Encode a URL', False),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'Which event occurs when a user clicks an HTML element?',
                'options': [
                    ('A) onmouseclick', False),
                    ('B) onclick', True),
                    ('C) onchange', False),
                    ('D) onhover', False)
                ]
            },
            {
                'text': 'Which keyword is used to define a function?',
                'options': [
                    ('A) function', True),
                    ('B) def', False),
                    ('C) func', False),
                    ('D) method', False)
                ]
            },
            {
                'text': 'What does the === operator check?',
                'options': [
                    ('A) Equal values', False),
                    ('B) Equal values and type', True),
                    ('C) Equal types only', False),
                    ('D) Greater than or equal', False)
                ]
            },
            {
                'text': 'What is the purpose of this keyword?',
                'options': [
                    ('A) Refers to the current object', True),
                    ('B) Refers to the global object', False),
                    ('C) Refers to a function parameter', False),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'Which JavaScript loop executes at least once?',
                'options': [
                    ('A) for', False),
                    ('B) do...while', True),
                    ('C) while', False),
                    ('D) forEach', False)
                ]
            },
            {
                'text': 'How do you create a promise in JavaScript?',
                'options': [
                    ('A) let promise = new Promise();', False),
                    ('B) let promise = Promise();', False),
                    ('C) let promise = new Promise((resolve, reject) => {});', True),
                    ('D) promise.create();', False)
                ]
            },
            {
                'text': 'How can you convert a string to an integer?',
                'options': [
                    ('A) Number.parse()', False),
                    ('B) parseInt()', True),
                    ('C) toInteger()', False),
                    ('D) convertInt()', False)
                ]
            },
            {
                'text': 'What is a callback function?',
                'options': [
                    ('A) A function passed as an argument to another function', True),
                    ('B) A function that returns another function', False),
                    ('C) A built-in function', False),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'What does the map() method do?',
                'options': [
                    ('A) Iterates over an array and transforms it', True),
                    ('B) Filters elements from an array', False),
                    ('C) Adds elements to an array', False),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'Which of the following is a JavaScript framework?',
                'options': [
                    ('A) Django', False),
                    ('B) Angular', True),
                    ('C) Flask', False),
                    ('D) Laravel', False)
                ]
            },
        ]

        self._create_questions(js_quiz, js_questions)

        # C Programming Quiz
        c_quiz = Quiz.objects.create(
            title='C Programming Basics',
            description='Dive into the essential concepts of C programming, including data types, control structures, functions, and memory management, and test your knowledge with this engaging quiz.',
            duration=30
        )

        c_questions = [
            {
                'text': 'What is the correct file extension for C programs?',
                'options': [
                    ('A) .cpp', False),
                    ('B) .c', True),
                    ('C) .h', False),
                    ('D) .cs', False)
                ]
            },
            {
                'text': 'What is the correct syntax to include a standard header file?',
                'options': [
                    ('A) #include "stdio.h"', False),
                    ('B) include <stdio>', False),
                    ('C) #include <stdio.h>', True),
                    ('D) import <stdio.h>', False)
                ]
            },
            {
                'text': 'What does int main() signify in a C program?',
                'options': [
                    ('A) The program\'s starting point', True),
                    ('B) A library function', False),
                    ('C) A preprocessor directive', False),
                    ('D) An error', False)
                ]
            },
            {
                'text': 'How do you declare a variable in C?',
                'options': [
                    ('A) var x = 10;', False),
                    ('B) int x = 10;', True),
                    ('C) x = 10;', False),
                    ('D) declare x = 10;', False)
                ]
            },
            {
                'text': 'Which symbol is used to end a statement in C?',
                'options': [
                    ('A) .', False),
                    ('B) :', False),
                    ('C) ;', True),
                    ('D) ,', False)
                ]
            },
            {
                'text': 'Which operator is used for assignment in C?',
                'options': [
                    ('A) ==', False),
                    ('B) =', True),
                    ('C) +=', False),
                    ('D) :', False)
                ]
            },
            {
                'text': 'What is the output of printf("%d", 5 + 3);?',
                'options': [
                    ('A) 5 + 3', False),
                    ('B) 8', True),
                    ('C) %d', False),
                    ('D) Error', False)
                ]
            },
            {
                'text': 'Which of the following is a valid data type in C?',
                'options': [
                    ('A) int', False),
                    ('B) float', False),
                    ('C) char', False),
                    ('D) All of the above', True)
                ]
            },
            {
                'text': 'What is the size of an int data type in C (typically)?',
                'options': [
                    ('A) 1 byte', False),
                    ('B) 2 bytes', False),
                    ('C) 4 bytes', True),
                    ('D) 8 bytes', False)
                ]
            },
            {
                'text': 'What does the scanf() function do?',
                'options': [
                    ('A) Prints output', False),
                    ('B) Reads input', True),
                    ('C) Executes code', False),
                    ('D) Declares variables', False)
                ]
            },
            {
                'text': 'Which keyword is used to define a constant in C?',
                'options': [
                    ('A) const', True),
                    ('B) let', False),
                    ('C) constant', False),
                    ('D) static', False)
                ]
            },
            {
                'text': 'What is the purpose of the return statement in main()?',
                'options': [
                    ('A) Ends the program', False),
                    ('B) Returns a value to the operating system', True),
                    ('C) Declares a function', False),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'Which loop ensures at least one execution of its block?',
                'options': [
                    ('A) for', False),
                    ('B) while', False),
                    ('C) do...while', True),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'What does the break statement do?',
                'options': [
                    ('A) Terminates the program', False),
                    ('B) Exits the current loop', True),
                    ('C) Restarts the loop', False),
                    ('D) Continues to the next iteration', False)
                ]
            },
            {
                'text': 'How do you declare a pointer in C?',
                'options': [
                    ('A) int ptr;', False),
                    ('B) int *ptr;', True),
                    ('C) int &ptr;', False),
                    ('D) ptr int;', False)
                ]
            },
            {
                'text': 'What is the result of 5 % 2 in C?',
                'options': [
                    ('A) 2', False),
                    ('B) 1', True),
                    ('C) 0', False),
                    ('D) Error', False)
                ]
            },
            {
                'text': 'What does sizeof operator return?',
                'options': [
                    ('A) The size of a data type or variable in bytes', True),
                    ('B) The length of a string', False),
                    ('C) The number of elements in an array', False),
                    ('D) None of the above', False)
                ]
            },
            {
                'text': 'How do you access the value of a variable through a pointer?',
                'options': [
                    ('A) ptr', False),
                    ('B) *ptr', True),
                    ('C) &ptr', False),
                    ('D) ptr.value', False)
                ]
            },
            {
                'text': 'What is the output of this code?\nint x = 10;\nprintf("%d", ++x);',
                'options': [
                    ('A) 10', False),
                    ('B) 11', True),
                    ('C) Error', False),
                    ('D) Undefined', False)
                ]
            },
            {
                'text': 'Which function is used to allocate memory dynamically in C?',
                'options': [
                    ('A) malloc()', False),
                    ('B) calloc()', False),
                    ('C) realloc()', False),
                    ('D) All of the above', True)
                ]
            },
        ]

        self._create_questions(c_quiz, c_questions)

        # Networking Quiz
        networking_quiz = Quiz.objects.create(
            title='Networking Basics',
            description='Dive into the fundamentals of networking and test your knowledge with this engaging quiz.',
            duration=30
        )

        networking_questions = [
            {
                'text': 'What does the acronym "IP" stand for in networking?',
                'options': [
                    ('A. Internet Provider', False),
                    ('B. Internet Protocol', True),
                    ('C. Internal Process', False),
                    ('D. Information Packet', False)
                ]
            },
            {
                'text': 'Which device is used to connect multiple computers in a network?',
                'options': [
                    ('A. Router', False),
                    ('B. Switch', True),
                    ('C. Modem', False),
                    ('D. Firewall', False)
                ]
            },
            {
                'text': 'What is the main function of a router?',
                'options': [
                    ('A. Connect devices within a LAN', False),
                    ('B. Forward data packets between networks', True),
                    ('C. Provide IP addresses', False),
                    ('D. Encrypt data for secure communication', False)
                ]
            },
            {
                'text': 'Which of the following is a common wired networking medium?',
                'options': [
                    ('A. Fiber-optic cable', True),
                    ('B. Bluetooth', False),
                    ('C. Wi-Fi', False),
                    ('D. Infrared', False)
                ]
            },
            {
                'text': 'What is the default port number for HTTP?',
                'options': [
                    ('A. 25', False),
                    ('B. 80', True),
                    ('C. 110', False),
                    ('D. 443', False)
                ]
            },
            {
                'text': 'What does DNS stand for?',
                'options': [
                    ('A. Domain Name System', True),
                    ('B. Digital Network Server', False),
                    ('C. Data Name Service', False),
                    ('D. Directory Network System', False)
                ]
            },
            {
                'text': 'Which protocol is used for email transmission?',
                'options': [
                    ('A. FTP', False),
                    ('B. SMTP', True),
                    ('C. HTTP', False),
                    ('D. SSH', False)
                ]
            },
            {
                'text': 'What is a MAC address?',
                'options': [
                    ('A. A unique identifier for a device on a network', True),
                    ('B. A type of IP address', False),
                    ('C. An address for connecting to websites', False),
                    ('D. An address used by DNS servers', False)
                ]
            },
            {
                'text': 'Which layer of the OSI model handles error detection and correction?',
                'options': [
                    ('A. Application', False),
                    ('B. Transport', False),
                    ('C. Data Link', True),
                    ('D. Network', False)
                ]
            },
            {
                'text': 'What type of network is restricted to a single building or campus?',
                'options': [
                    ('A. WAN', False),
                    ('B. LAN', True),
                    ('C. MAN', False),
                    ('D. PAN', False)
                ]
            },
            {
                'text': 'What is the primary purpose of a firewall?',
                'options': [
                    ('A. Speed up network connections', False),
                    ('B. Protect a network from unauthorized access', True),
                    ('C. Distribute IP addresses', False),
                    ('D. Store data for a network', False)
                ]
            },
            {
                'text': 'Which protocol is used to securely transfer files over a network?',
                'options': [
                    ('A. FTP', False),
                    ('B. SFTP', True),
                    ('C. HTTP', False),
                    ('D. POP3', False)
                ]
            },
            {
                'text': 'What does the term "bandwidth" refer to?',
                'options': [
                    ('A. The length of a network cable', False),
                    ('B. The speed of a network', False),
                    ('C. The amount of data a network can transmit in a given time', True),
                    ('D. The number of connected devices', False)
                ]
            },
            {
                'text': 'Which of the following is a private IP address?',
                'options': [
                    ('A. 192.168.1.1', True),
                    ('B. 8.8.8.8', False),
                    ('C. 123.45.67.89', False),
                    ('D. 172.217.16.14', False)
                ]
            },
            {
                'text': 'Which protocol translates a domain name into an IP address?',
                'options': [
                    ('A. FTP', False),
                    ('B. DHCP', False),
                    ('C. DNS', True),
                    ('D. HTTP', False)
                ]
            },
            {
                'text': 'What is the purpose of a subnet mask?',
                'options': [
                    ('A. Identify network boundaries', True),
                    ('B. Encrypt network traffic', False),
                    ('C. Assign IP addresses dynamically', False),
                    ('D. Boost network speed', False)
                ]
            },
            {
                'text': 'Which layer of the OSI model is responsible for end-to-end communication?',
                'options': [
                    ('A. Transport', True),
                    ('B. Network', False),
                    ('C. Application', False),
                    ('D. Session', False)
                ]
            },
            {
                'text': 'What is the maximum length of a UTP Ethernet cable?',
                'options': [
                    ('A. 50 meters', False),
                    ('B. 100 meters', True),
                    ('C. 150 meters', False),
                    ('D. 200 meters', False)
                ]
            },
            {
                'text': 'Which protocol is used to access a remote computer securely?',
                'options': [
                    ('A. HTTP', False),
                    ('B. SSH', True),
                    ('C. FTP', False),
                    ('D. Telnet', False)
                ]
            },
            {
                'text': 'What is a VLAN?',
                'options': [
                    ('A. Virtual Link Access Network', False),
                    ('B. Virtual Local Area Network', True),
                    ('C. Vast Local Access Node', False),
                    ('D. Variable LAN Address', False)
                ]
            },
        ]

        self._create_questions(networking_quiz, networking_questions)

    def _create_questions(self, quiz, questions_data):
        for q_data in questions_data:
            question = Question.objects.create(
                quiz=quiz,
                question_text=q_data['text']
            )
            
            for option_text, is_correct in q_data['options']:
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )