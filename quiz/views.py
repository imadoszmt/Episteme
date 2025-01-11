import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Quiz, Question, UserAnswer, Option, QuizAttempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.http import JsonResponse
import re

def home(request):
    return render(request, 'home.html')

# Custom logout view
def direct_logout(request):
    logout(request)
    return redirect('/')  # Redirect to homepage or desired URL

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz.html', {'quiz': quiz})

@login_required
def quiz_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    
    if request.method == 'POST':
        selected_option = request.POST.get('answer')
        if selected_option:
            UserAnswer.objects.create(
                user=request.user,
                quiz=quiz,
                question=question,
                selected_option_id=selected_option
            )
            next_question = quiz.get_next_question(question)
            if next_question:
                return redirect('quiz_question', quiz_id=quiz.id, question_id=next_question.id)
            return redirect('quiz_results', quiz_id=quiz.id)
    
    context = {
        'quiz': quiz,
        'question': question,
        'current_question_no': quiz.get_question_number(question),
        'total_questions': quiz.questions.count(),
        'progress': quiz.get_progress(question),
        'prev_question': quiz.get_previous_question(question),
        'is_last_question': quiz.is_last_question(question)
    }
    return render(request, 'quiz.html', context)

#@login_required
#def quiz_results(request, quiz_id):
    #quiz = get_object_or_404(Quiz, id=quiz_id)
    #user_answers = UserAnswer.objects.filter(user=request.user, quiz=quiz)
    
    #correct_answers = sum(1 for answer in user_answers if answer.is_correct())
    #total_questions = quiz.questions.count()
    #score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Save the score in the UserAnswer model
    #for answer in user_answers:
        #answer.score = score  # Assign the score to each answer
        #answer.save()

    #context = {
        #'quiz': quiz,
        #'score': round(score, 1),
        #'correct_answers': correct_answers,
        #'total_questions': total_questions,
        #'user_answers': user_answers
    #}
    #return render(request, 'results.html', context)
@login_required
def quiz_results(request, attempt_id):
    quiz_attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz'), id=attempt_id)
    
    # Ensure user can only view their own results
    if quiz_attempt.user != request.user:
        return redirect('home')
    
    user_answers = quiz_attempt.answers.all().select_related(
        'question',
        'selected_option'
    )
    
    context = {
        'quiz_attempt': quiz_attempt,
        'score': quiz_attempt.score,
        'user_answers': user_answers,
        'total_questions': user_answers.count(),
        'correct_answers': sum(1 for answer in user_answers if answer.selected_option.is_correct)
    }
    
    return render(request, 'results.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

#@login_required
#def account_profile(request):
    #quiz_attempts = UserAnswer.objects.filter(user=request.user).select_related('quiz').order_by('-created_at')  # Fetch quiz attempts
    #return render(request, 'account/profile.html', {'quiz_attempts': quiz_attempts})
@login_required
def profile_view(request):
    # Get user's quiz attempts with related quiz information
    quiz_attempts = QuizAttempt.objects.filter(user=request.user)\
        .select_related('quiz')\
        .order_by('-created_at')
    
    context = {
        'quiz_attempts': quiz_attempts,
        'user': request.user
    }
    return render(request, 'account/profile.html', context)

@login_required
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers_data = request.POST.get('answers', None)
    
    if not answers_data:
        return JsonResponse({'error': 'No answers provided'}, status=400)
    
    try:
        answers = json.loads(answers_data)
        total_questions = quiz.questions.count()
        correct_answers = 0
        
        # Create quiz attempt
        quiz_attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0  # Will be updated after calculating
        )
        
        # Process each answer
        for question_id, option_id in answers.items():
            question = Question.objects.get(id=question_id)
            selected_option = Option.objects.get(id=option_id)
            
            # Save user's answer
            UserAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_option=selected_option
            )
            
            # Count correct answers
            if selected_option.is_correct:
                correct_answers += 1
        
        # Calculate and update score
        score = (correct_answers / total_questions) * 100
        quiz_attempt.score = round(score)
        quiz_attempt.save()
        
        return JsonResponse({
            'success': True,
            'score': quiz_attempt.score,
            'redirect_url': reverse('quiz_results', args=[quiz_attempt.id])
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         # Validate email format
#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             messages.error(request, 'Invalid email format.')
#             return render(request, 'account/signup.html')

#         # Validate username uniqueness
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#             return render(request, 'account/signup.html')

#         # Validate password complexity
#         if len(password1) < 8:  # Check for minimum length
#             messages.error(request, 'Password must be at least 8 characters long.')
#             return render(request, 'account/signup.html')

#         if not re.search(r"[A-Za-z]", password1):  # Check for letters
#             messages.error(request, 'Password must contain at least one letter.')
#             return render(request, 'account/signup.html')

#         if not re.search(r"\d", password1):  # Check for numbers
#             messages.error(request, 'Password must contain at least one number.')
#             return render(request, 'account/signup.html')

#         if password1.isdigit():  # Check if password is purely numeric
#             messages.error(request, 'Password cannot be entirely numeric.')
#             return render(request, 'account/signup.html')

#         # Check if passwords match
#         if password1 == password2:
#             try:
#                 user = User.objects.create_user(username=username, email=email, password=password1)
#                 user.save()
#                 login(request, user)  # Log the user in after registration
#                 messages.success(request, 'Account created successfully! Redirecting to your profile...')
#                 return redirect('account_profile')  # Redirect to the profile page
#             except Exception as e:
#                 messages.error(request, f'Error creating account: {e}')
#         else:
#             messages.error(request, 'Passwords do not match.')
#     return render(request, 'account/signup.html')
# # End of Selection

#def login_view(request):
    #if request.method == 'POST':
        #login_param = request.POST.get('login')  # This can be username or email
        #password = request.POST.get('password')
        #user = authenticate(request, username=login_param, password=password)
        #if user is not None:
            #login(request, user)
            #return redirect('account_profile')  # Redirect to profile after login
        #else:
            #messages.error(request, 'Invalid username or password.')
    #return render(request, 'account/login.html')

def networking_quiz(request):
    questions = [
        {
            'text': 'What does the acronym "IP" stand for in networking?',
            'options': ['A. Internet Provider', 'B. Internet Protocol', 'C. Internal Process', 'D. Information Packet'],
            'correct_answer': 'B. Internet Protocol'
        },
        {
            'text': 'Which device is used to connect multiple computers in a network?',
            'options': ['A. Router', 'B. Switch', 'C. Modem', 'D. Firewall'],
            'correct_answer': 'B. Switch'
        },
        {
            'text': 'What is the main function of a router?',
            'options': ['A. Connect devices within a LAN', 'B. Forward data packets between networks', 'C. Provide IP addresses', 'D. Encrypt data for secure communication'],
            'correct_answer': 'B. Forward data packets between networks'
        },
        {
            'text': 'Which of the following is a common wired networking medium?',
            'options': ['A. Fiber-optic cable', 'B. Bluetooth', 'C. Wi-Fi', 'D. Infrared'],
            'correct_answer': 'A. Fiber-optic cable'
        },
        {
            'text': 'What is the default port number for HTTP?',
            'options': ['A. 25', 'B. 80', 'C. 110', 'D. 443'],
            'correct_answer': 'B. 80'
        },
        {
            'text': 'What does DNS stand for?',
            'options': ['A. Domain Name System', 'B. Digital Network Server', 'C. Data Name Service', 'D. Directory Network System'],
            'correct_answer': 'A. Domain Name System'
        },
        {
            'text': 'Which protocol is used for email transmission?',
            'options': ['A. FTP', 'B. SMTP', 'C. HTTP', 'D. SSH'],
            'correct_answer': 'B. SMTP'
        },
        {
            'text': 'What is a MAC address?',
            'options': ['A. A unique identifier for a device on a network', 'B. A type of IP address', 'C. An address for connecting to websites', 'D. An address used by DNS servers'],
            'correct_answer': 'A. A unique identifier for a device on a network'
        },
        {
            'text': 'Which layer of the OSI model handles error detection and correction?',
            'options': ['A. Application', 'B. Transport', 'C. Data Link', 'D. Network'],
            'correct_answer': 'C. Data Link'
        },
        {
            'text': 'What type of network is restricted to a single building or campus?',
            'options': ['A. WAN', 'B. LAN', 'C. MAN', 'D. PAN'],
            'correct_answer': 'B. LAN'
        },
        {
            'text': 'What is the primary purpose of a firewall?',
            'options': ['A. Speed up network connections', 'B. Protect a network from unauthorized access', 'C. Distribute IP addresses', 'D. Store data for a network'],
            'correct_answer': 'B. Protect a network from unauthorized access'
        },
        {
            'text': 'Which protocol is used to securely transfer files over a network?',
            'options': ['A. FTP', 'B. SFTP', 'C. HTTP', 'D. POP3'],
            'correct_answer': 'B. SFTP'
        },
        {
            'text': 'What does the term "bandwidth" refer to?',
            'options': ['A. The length of a network cable', 'B. The speed of a network', 'C. The amount of data a network can transmit in a given time', 'D. The number of connected devices'],
            'correct_answer': 'C. The amount of data a network can transmit in a given time'
        },
        {
            'text': 'Which of the following is a private IP address?',
            'options': ['A. 192.168.1.1', 'B. 8.8.8.8', 'C. 123.45.67.89', 'D. 172.217.16.14'],
            'correct_answer': 'A. 192.168.1.1'
        },
        {
            'text': 'Which protocol translates a domain name into an IP address?',
            'options': ['A. FTP', 'B. DHCP', 'C. DNS', 'D. HTTP'],
            'correct_answer': 'C. DNS'
        },
        {
            'text': 'What is the purpose of a subnet mask?',
            'options': ['A. Identify network boundaries', 'B. Encrypt network traffic', 'C. Assign IP addresses dynamically', 'D. Boost network speed'],
            'correct_answer': 'A. Identify network boundaries'
        },
        {
            'text': 'Which layer of the OSI model is responsible for end-to-end communication?',
            'options': ['A. Transport', 'B. Network', 'C. Application', 'D. Session'],
            'correct_answer': 'A. Transport'
        },
        {
            'text': 'What is the maximum length of a UTP Ethernet cable?',
            'options': ['A. 50 meters', 'B. 100 meters', 'C. 150 meters', 'D. 200 meters'],
            'correct_answer': 'B. 100 meters'
        },
        {
            'text': 'Which protocol is used to access a remote computer securely?',
            'options': ['A. HTTP', 'B. SSH', 'C. FTP', 'D. Telnet'],
            'correct_answer': 'B. SSH'
        },
        {
            'text': 'What is a VLAN?',
            'options': ['A. Virtual Link Access Network', 'B. Virtual Local Area Network', 'C. Vast Local Access Node', 'D. Variable LAN Address'],
            'correct_answer': 'B. Virtual Local Area Network'
        },
    ]
    return render(request, 'quiz/networking_quiz.html', {'questions': questions})

def web_programming_quiz(request):
    questions = [
        {
            'text': 'Which of the following is NOT a web browser?',
            'options': ['A. Chrome', 'B. Firefox', 'C. Edge', 'D. Python'],
            'correct_answer': 'D. Python'
        },
        {
            'text': 'What does HTTP stand for?',
            'options': ['A. HyperText Transmission Protocol', 'B. HyperText Transfer Protocol', 'C. HighText Transfer Protocol', 'D. HyperText Transfer Packet'],
            'correct_answer': 'B. HyperText Transfer Protocol'
        },
        {
            'text': 'What is the correct HTML element for the largest heading?',
            'options': ['A. <h1>', 'B. <h6>', 'C. <header>', 'D. <h0>'],
            'correct_answer': 'A. <h1>'
        },
        {
            'text': 'Which HTML attribute is used to define inline styles?',
            'options': ['A. class', 'B. style', 'C. id', 'D. css'],
            'correct_answer': 'B. style'
        },
        {
            'text': 'Which property is used in CSS to change text color?',
            'options': ['A. color', 'B. font-color', 'C. text-color', 'D. background-color'],
            'correct_answer': 'A. color'
        },
        {
            'text': 'What does the "C" in CSS stand for?',
            'options': ['A. Complex', 'B. Cascading', 'C. Creative', 'D. Custom'],
            'correct_answer': 'B. Cascading'
        },
        {
            'text': 'Which tag is used for adding a line break in HTML?',
            'options': ['A. <break>', 'B. <lb>', 'C. <br>', 'D. <line>'],
            'correct_answer': 'C. <br>'
        },
        {
            'text': 'What does <ul> represent in HTML?',
            'options': ['A. Underline', 'B. Unordered List', 'C. Uniform Layout', 'D. User List'],
            'correct_answer': 'B. Unordered List'
        },
        {
            'text': 'What is the default method for submitting forms in HTML?',
            'options': ['A. GET', 'B. POST', 'C. PUT', 'D. DELETE'],
            'correct_answer': 'A. GET'
        },
        {
            'text': 'Which of the following is NOT a JavaScript framework?',
            'options': ['A. Angular', 'B. React', 'C. Django', 'D. Vue'],
            'correct_answer': 'C. Django'
        },
        {
            'text': 'In CSS, what does z-index control?',
            'options': ['A. The zoom level', 'B. The stacking order of elements', 'C. The size of the element', 'D. The background image'],
            'correct_answer': 'B. The stacking order of elements'
        },
        {
            'text': 'What is the purpose of the <meta> tag in HTML?',
            'options': ['A. Adding links to external stylesheets', 'B. Storing metadata about the webpage', 'C. Inserting media elements', 'D. Embedding JavaScript'],
            'correct_answer': 'B. Storing metadata about the webpage'
        },
        {
            'text': 'What is Bootstrap used for?',
            'options': ['A. Database management', 'B. Front-end framework for responsive design', 'C. Back-end server handling', 'D. Debugging JavaScript'],
            'correct_answer': 'B. Front-end framework for responsive design'
        },
        {
            'text': 'What does <iframe> do in HTML?',
            'options': ['A. Embeds a video', 'B. Embeds another HTML page', 'C. Creates a pop-up window', 'D. Creates a scrollable region'],
            'correct_answer': 'B. Embeds another HTML page'
        },
        {
            'text': 'Which CSS property is used to make text bold?',
            'options': ['A. weight', 'B. font-weight', 'C. bold', 'D. text-style'],
            'correct_answer': 'B. font-weight'
        },
        {
            'text': 'What is a favicon?',
            'options': ['A. A small image displayed in the browser tab', 'B. A type of button', 'C. An external link', 'D. A navigation icon'],
            'correct_answer': 'A. A small image displayed in the browser tab'
        },
        {
            'text': 'What does the <title> tag do?',
            'options': ['A. Displays text in the header', 'B. Sets the title of the document in the browser tab', 'C. Creates a heading', 'D. Sets metadata'],
            'correct_answer': 'B. Sets the title of the document in the browser tab'
        },
        {
            'text': 'Which tag is used to insert an image in HTML?',
            'options': ['A. <img>', 'B. <image>', 'C. <pic>', 'D. <media>'],
            'correct_answer': 'A. <img>'
        },
        {
            'text': 'What is the primary purpose of the <nav> element in HTML?',
            'options': ['A. To include navigation links', 'B. To display images', 'C. To embed videos', 'D. To create lists'],
            'correct_answer': 'A. To include navigation links'
        },
        {
            'text': 'What is the correct syntax for linking an external CSS file?',
            'options': ['A. <link rel="stylesheet" href="style.css">', 'B. <style href="style.css">', 'C. <css src="style.css">', 'D. <stylesheet link="style.css">'],
            'correct_answer': 'A. <link rel="stylesheet" href="style.css">'
        },
    ]
    return render(request, 'quiz/web_programming_quiz.html', {'questions': questions})

def database_quiz(request):
    questions = [
        {
            'text': 'What does a relational database store data in?',
            'options': ['A) Arrays', 'B) Tables', 'C) Graphs', 'D) Files'],
            'correct_answer': 'B) Tables'
        },
        {
            'text': 'What does DDL stand for in SQL?',
            'options': ['A) Data Description Language', 'B) Data Definition Language', 'C) Database Design Language', 'D) Data Deployment Language'],
            'correct_answer': 'B) Data Definition Language'
        },
        {
            'text': 'Which SQL command is used to remove all records from a table?',
            'options': ['A) DELETE', 'B) DROP', 'C) CLEAR', 'D) TRUNCATE'],
            'correct_answer': 'D) TRUNCATE'
        },
        {
            'text': 'What is a database index used for?',
            'options': ['A) Sorting data', 'B) Increasing retrieval speed', 'C) Adding constraints', 'D) Storing temporary data'],
            'correct_answer': 'B) Increasing retrieval speed'
        },
        {
            'text': 'Which of the following is NOT a type of database?',
            'options': ['A) Hierarchical', 'B) Relational', 'C) Network', 'D) Sequential'],
            'correct_answer': 'D) Sequential'
        },
        {
            'text': 'What is a database schema?',
            'options': ['A) The data stored in a table', 'B) A visual representation of data', 'C) The structure that defines a database', 'D) A backup of a database'],
            'correct_answer': 'C) The structure that defines a database'
        },
        {
            'text': 'What does ACID stand for in databases?',
            'options': ['A) Atomicity, Consistency, Isolation, Durability', 'B) Accuracy, Consistency, Integrity, Dependability', 'C) Access, Control, Integration, Durability', 'D) Atomicity, Control, Isolation, Dependency'],
            'correct_answer': 'A) Atomicity, Consistency, Isolation, Durability'
        },
        {
            'text': 'Which SQL clause is used to filter records?',
            'options': ['A) WHERE', 'B) FILTER', 'C) SEARCH', 'D) FIND'],
            'correct_answer': 'A) WHERE'
        },
        {
            'text': 'What is the function of a foreign key?',
            'options': ['A) Link two tables', 'B) Encrypt data', 'C) Sort records', 'D) Add uniqueness to a column'],
            'correct_answer': 'A) Link two tables'
        },
        {
            'text': 'What is a NULL value in a database?',
            'options': ['A) A default value', 'B) A missing or undefined value', 'C) A zero value', 'D) A deleted record'],
            'correct_answer': 'B) A missing or undefined value'
        },
        {
            'text': 'Which SQL keyword is used to sort results?',
            'options': ['A) ORDER BY', 'B) SORT BY', 'C) GROUP BY', 'D) ARRANGE'],
            'correct_answer': 'A) ORDER BY'
        },
        {
            'text': 'What is a view in a database?',
            'options': ['A) A temporary table', 'B) A virtual table based on SQL query results', 'C) A stored procedure', 'D) A graphical representation of a table'],
            'correct_answer': 'B) A virtual table based on SQL query results'
        },
        {
            'text': 'Which of the following is a NoSQL database?',
            'options': ['A) MySQL', 'B) MongoDB', 'C) PostgreSQL', 'D) SQLite'],
            'correct_answer': 'B) MongoDB'
        },
        {
            'text': 'What is the purpose of normalization in databases?',
            'options': ['A) Reduce redundancy and improve data integrity', 'B) Increase storage space', 'C) Add more tables', 'D) Increase retrieval speed'],
            'correct_answer': 'A) Reduce redundancy and improve data integrity'
        },
        {
            'text': 'What does a JOIN clause do in SQL?',
            'options': ['A) Deletes data', 'B) Combines rows from two or more tables', 'C) Updates records', 'D) Creates a new table'],
            'correct_answer': 'B) Combines rows from two or more tables'
        },
        {
            'text': 'What is a stored procedure?',
            'options': ['A) A predefined SQL function stored in the database', 'B) A temporary table', 'C) A database schema', 'D) A unique key'],
            'correct_answer': 'A) A predefined SQL function stored in the database'
        },
        {
            'text': 'What is the function of the SQL GROUP BY clause?',
            'options': ['A) Filter rows', 'B) Aggregate data into groups', 'C) Sort records', 'D) Create new tables'],
            'correct_answer': 'B) Aggregate data into groups'
        },
        {
            'text': 'What does the DISTINCT keyword do in SQL?',
            'options': ['A) Removes duplicate records', 'B) Adds a unique constraint', 'C) Defines a primary key', 'D) Deletes records'],
            'correct_answer': 'A) Removes duplicate records'
        },
        {
            'text': 'What is a database transaction?',
            'options': ['A) A single unit of work in a database', 'B) A backup process', 'C) A query to retrieve data', 'D) An SQL command for creating tables'],
            'correct_answer': 'A) A single unit of work in a database'
        },
        {
            'text': 'Which of these is a database constraint?',
            'options': ['A) PRIMARY KEY', 'B) FOREIGN KEY', 'C) UNIQUE', 'D) All of the above'],
            'correct_answer': 'D) All of the above'
        },
    ]
    return render(request, 'quiz/database_quiz.html', {'questions': questions})

def python_quiz(request):
    questions = [
        {
            'text': 'What is the correct file extension for Python files?',
            'options': ['A) .py', 'B) .pt', 'C) .python', 'D) .pyt'],
            'correct_answer': 'A) .py'
        },
        {
            'text': 'Which function is used to display output in Python?',
            'options': ['A) echo()', 'B) display()', 'C) print()', 'D) show()'],
            'correct_answer': 'C) print()'
        },
        {
            'text': 'What is the result of 3 ** 2 in Python?',
            'options': ['A) 5', 'B) 6', 'C) 9', 'D) 8'],
            'correct_answer': 'C) 9'
        },
        {
            'text': 'Which of the following is a Python data type?',
            'options': ['A) String', 'B) List', 'C) Dictionary', 'D) All of the above'],
            'correct_answer': 'D) All of the above'
        },
        {
            'text': 'How do you start a comment in Python?',
            'options': ['A) //', 'B) /*', 'C) #', 'D) <!--'],
            'correct_answer': 'C) #'
        },
        {
            'text': 'What is the output of len("Hello")?',
            'options': ['A) 4', 'B) 5', 'C) 6', 'D) Error'],
            'correct_answer': 'B) 5'
        },
        {
            'text': 'What is the purpose of the input() function?',
            'options': ['A) Display output', 'B) Accept user input', 'C) Terminate the program', 'D) Repeat a process'],
            'correct_answer': 'B) Accept user input'
        },
        {
            'text': 'What is the correct way to create a list in Python?',
            'options': ['A) {1, 2, 3}', 'B) [1, 2, 3]', 'C) (1, 2, 3)', 'D) <1, 2, 3>'],
            'correct_answer': 'B) [1, 2, 3]'
        },
        {
            'text': 'What is the output of 5 // 2?',
            'options': ['A) 2', 'B) 2.5', 'C) 3', 'D) Error'],
            'correct_answer': 'A) 2'
        },
        {
            'text': 'How do you define a function in Python?',
            'options': ['A) function myFunc()', 'B) def myFunc():', 'C) func myFunc()', 'D) myFunc():'],
            'correct_answer': 'B) def myFunc():'
        },
        {
            'text': 'Which keyword is used to create a class in Python?',
            'options': ['A) define', 'B) func', 'C) class', 'D) object'],
            'correct_answer': 'C) class'
        },
        {
            'text': 'What is a tuple in Python?',
            'options': ['A) A mutable sequence', 'B) An immutable sequence', 'C) A function', 'D) A string'],
            'correct_answer': 'B) An immutable sequence'
        },
        {
            'text': 'What is the output of bool(0) in Python?',
            'options': ['A) True', 'B) False', 'C) None', 'D) Error'],
            'correct_answer': 'B) False'
        },
        {
            'text': 'What does break do in a loop?',
            'options': ['A) Skips the current iteration', 'B) Exits the loop', 'C) Restarts the loop', 'D) Ends the program'],
            'correct_answer': 'B) Exits the loop'
        },
        {
            'text': 'Which keyword is used to handle exceptions in Python?',
            'options': ['A) catch', 'B) except', 'C) error', 'D) trycatch'],
            'correct_answer': 'B) except'
        },
        {
            'text': 'What is the correct way to import a module in Python?',
            'options': ['A) import module_name', 'B) use module_name', 'C) include module_name', 'D) require module_name'],
            'correct_answer': 'A) import module_name'
        },
        {
            'text': 'What does None represent in Python?',
            'options': ['A) A number', 'B) A string', 'C) A null value', 'D) An error'],
            'correct_answer': 'C) A null value'
        },
        {
            'text': 'How do you access the first element of a list my_list?',
            'options': ['A) my_list[0]', 'B) my_list[1]', 'C) my_list[-1]', 'D) my_list.first()'],
            'correct_answer': 'A) my_list[0]'
        },
        {
            'text': 'What is the purpose of the range() function?',
            'options': ['A) Create strings', 'B) Iterate over numbers', 'C) Generate random numbers', 'D) Sort lists'],
            'correct_answer': 'B) Iterate over numbers'
        },
        {
            'text': 'Which of these is used to create a block of code in Python?',
            'options': ['A) Parentheses', 'B) Curly braces', 'C) Indentation', 'D) Square brackets'],
            'correct_answer': 'C) Indentation'
        },
    ]
    return render(request, 'quiz/python_quiz.html', {'questions': questions})

def javascript_quiz(request):
    questions = [
        {
            'text': 'What is the correct syntax to output "Hello, World!" in JavaScript?',
            'options': ['A) console.log("Hello, World!");', 'B) echo "Hello, World!";', 'C) print("Hello, World!");', 'D) write("Hello, World!");'],
            'correct_answer': 'A) console.log("Hello, World!");'
        },
        {
            'text': 'Which keyword is used to declare a variable in JavaScript?',
            'options': ['A) var', 'B) let', 'C) const', 'D) All of the above'],
            'correct_answer': 'D) All of the above'
        },
        {
            'text': 'What does typeof operator do in JavaScript?',
            'options': ['A) Defines a variable\'s type', 'B) Returns the data type of a variable', 'C) Converts data types', 'D) Checks for errors'],
            'correct_answer': 'B) Returns the data type of a variable'
        },
        {
            'text': 'What is the value of NaN in JavaScript?',
            'options': ['A) null', 'B) undefined', 'C) Not a Number', 'D) Zero'],
            'correct_answer': 'C) Not a Number'
        },
        {
            'text': 'How do you write a comment in JavaScript?',
            'options': ['A) // This is a comment', 'B) <!-- This is a comment -->', 'C) # This is a comment', 'D) /* This is a comment */'],
            'correct_answer': 'A) // This is a comment'
        },
        {
            'text': 'Which method is used to round a number to the nearest integer?',
            'options': ['A) Math.ceil()', 'B) Math.floor()', 'C) Math.round()', 'D) Math.random()'],
            'correct_answer': 'C) Math.round()'
        },
        {
            'text': 'How do you declare an array in JavaScript?',
            'options': ['A) {1, 2, 3}', 'B) [1, 2, 3]', 'C) (1, 2, 3)', 'D) <1, 2, 3>'],
            'correct_answer': 'B) [1, 2, 3]'
        },
        {
            'text': 'What is the default value of an uninitialized variable in JavaScript?',
            'options': ['A) null', 'B) undefined', 'C) 0', 'D) false'],
            'correct_answer': 'B) undefined'
        },
        {
            'text': 'How do you add a new element to the end of an array?',
            'options': ['A) array.add()', 'B) array.push()', 'C) array.append()', 'D) array.insert()'],
            'correct_answer': 'B) array.push()'
        },
        {
            'text': 'What is the purpose of JSON.stringify()?',
            'options': ['A) Convert an object into a string', 'B) Parse a string into an object', 'C) Encode a URL', 'D) None of the above'],
            'correct_answer': 'A) Convert an object into a string'
        },
        {
            'text': 'Which event occurs when a user clicks an HTML element?',
            'options': ['A) onmouseclick', 'B) onclick', 'C) onchange', 'D) onhover'],
            'correct_answer': 'B) onclick'
        },
        {
            'text': 'Which keyword is used to define a function?',
            'options': ['A) function', 'B) def', 'C) func', 'D) method'],
            'correct_answer': 'A) function'
        },
        {
            'text': 'What does the === operator check?',
            'options': ['A) Equal values', 'B) Equal values and type', 'C) Equal types only', 'D) Greater than or equal'],
            'correct_answer': 'B) Equal values and type'
        },
        {
            'text': 'What is the purpose of this keyword?',
            'options': ['A) Refers to the current object', 'B) Refers to the global object', 'C) Refers to a function parameter', 'D) None of the above'],
            'correct_answer': 'A) Refers to the current object'
        },
        {
            'text': 'Which JavaScript loop executes at least once?',
            'options': ['A) for', 'B) do...while', 'C) while', 'D) forEach'],
            'correct_answer': 'B) do...while'
        },
        {
            'text': 'How do you create a promise in JavaScript?',
            'options': ['A) let promise = new Promise();', 'B) let promise = Promise();', 'C) let promise = new Promise((resolve, reject) => {});', 'D) promise.create();'],
            'correct_answer': 'C) let promise = new Promise((resolve, reject) => {});'
        },
        {
            'text': 'How can you convert a string to an integer?',
            'options': ['A) Number.parse()', 'B) parseInt()', 'C) toInteger()', 'D) convertInt()'],
            'correct_answer': 'B) parseInt()'
        },
        {
            'text': 'What is a callback function?',
            'options': ['A) A function passed as an argument to another function', 'B) A function that returns another function', 'C) A built-in function', 'D) None of the above'],
            'correct_answer': 'A) A function passed as an argument to another function'
        },
        {
            'text': 'What does the map() method do?',
            'options': ['A) Iterates over an array and transforms it', 'B) Filters elements from an array', 'C) Adds elements to an array', 'D) None of the above'],
            'correct_answer': 'A) Iterates over an array and transforms it'
        },
        {
            'text': 'Which of the following is a JavaScript framework?',
            'options': ['A) Django', 'B) Angular', 'C) Flask', 'D) Laravel'],
            'correct_answer': 'B) Angular'
        },
    ]
    return render(request, 'quiz/javascript_quiz.html', {'questions': questions})

def c_programming_quiz(request):
    questions = [
        {
            'text': 'What is the correct file extension for C programs?',
            'options': ['A) .cpp', 'B) .c', 'C) .h', 'D) .cs'],
            'correct_answer': 'B) .c'
        },
        {
            'text': 'What is the correct syntax to include a standard header file?',
            'options': ['A) #include "stdio.h"', 'B) include <stdio>', 'C) #include <stdio.h>', 'D) import <stdio.h>'],
            'correct_answer': 'C) #include <stdio.h>'
        },
        {
            'text': 'What does int main() signify in a C program?',
            'options': ['A) The program\'s starting point', 'B) A library function', 'C) A preprocessor directive', 'D) An error'],
            'correct_answer': 'A) The program\'s starting point'
        },
        {
            'text': 'How do you declare a variable in C?',
            'options': ['A) var x = 10;', 'B) int x = 10;', 'C) x = 10;', 'D) declare x = 10;'],
            'correct_answer': 'B) int x = 10;'
        },
        {
            'text': 'Which symbol is used to end a statement in C?',
            'options': ['A) .', 'B) :', 'C) ;', 'D) ,'],
            'correct_answer': 'C) ;'
        },
        {
            'text': 'Which operator is used for assignment in C?',
            'options': ['A) ==', 'B) =', 'C) +=', 'D) :'],
            'correct_answer': 'B) ='
        },
        {
            'text': 'What is the output of printf("%d", 5 + 3);?',
            'options': ['A) 5 + 3', 'B) 8', 'C) %d', 'D) Error'],
            'correct_answer': 'B) 8'
        },
        {
            'text': 'Which of the following is a valid data type in C?',
            'options': ['A) int', 'B) float', 'C) char', 'D) All of the above'],
            'correct_answer': 'D) All of the above'
        },
        {
            'text': 'What is the size of an int data type in C (typically)?',
            'options': ['A) 1 byte', 'B) 2 bytes', 'C) 4 bytes', 'D) 8 bytes'],
            'correct_answer': 'C) 4 bytes'
        },
        {
            'text': 'What does the scanf() function do?',
            'options': ['A) Prints output', 'B) Reads input', 'C) Executes code', 'D) Declares variables'],
            'correct_answer': 'B) Reads input'
        },
        {
            'text': 'Which keyword is used to define a constant in C?',
            'options': ['A) const', 'B) let', 'C) constant', 'D) static'],
            'correct_answer': 'A) const'
        },
        {
            'text': 'What is the purpose of the return statement in main()?',
            'options': ['A) Ends the program', 'B) Returns a value to the operating system', 'C) Declares a function', 'D) None of the above'],
            'correct_answer': 'B) Returns a value to the operating system'
        },
        {
            'text': 'Which loop ensures at least one execution of its block?',
            'options': ['A) for', 'B) while', 'C) do...while', 'D) None of the above'],
            'correct_answer': 'C) do...while'
        },
        {
            'text': 'What does the break statement do?',
            'options': ['A) Terminates the program', 'B) Exits the current loop', 'C) Restarts the loop', 'D) Continues to the next iteration'],
            'correct_answer': 'B) Exits the current loop'
        },
        {
            'text': 'How do you declare a pointer in C?',
            'options': ['A) int ptr;', 'B) int *ptr;', 'C) int &ptr;', 'D) ptr int;'],
            'correct_answer': 'B) int *ptr;'
        },
        {
            'text': 'What is the result of 5 % 2 in C?',
            'options': ['A) 2', 'B) 1', 'C) 0', 'D) Error'],
            'correct_answer': 'B) 1'
        },
        {
            'text': 'What does sizeof operator return?',
            'options': ['A) The size of a data type or variable in bytes', 'B) The length of a string', 'C) The number of elements in an array', 'D) None of the above'],
            'correct_answer': 'A) The size of a data type or variable in bytes'
        },
        {
            'text': 'How do you access the value of a variable through a pointer?',
            'options': ['A) ptr', 'B) *ptr', 'C) &ptr', 'D) ptr.value'],
            'correct_answer': 'B) *ptr'
        },
        {
            'text': 'What is the output of this code?\nint x = 10;\nprintf("%d", ++x);',
            'options': ['A) 10', 'B) 11', 'C) Error', 'D) Undefined'],
            'correct_answer': 'B) 11'
        },
        {
            'text': 'Which function is used to allocate memory dynamically in C?',
            'options': ['A) malloc()', 'B) calloc()', 'C) realloc()', 'D) All of the above'],
            'correct_answer': 'D) All of the above'
        },
    ]
    return render(request, 'quiz/c_programming_quiz.html', {'questions': questions})
