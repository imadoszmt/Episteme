from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, UserAnswer
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
import re

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

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

@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_answers = UserAnswer.objects.filter(user=request.user, quiz=quiz)
    
    correct_answers = sum(1 for answer in user_answers if answer.is_correct())
    total_questions = quiz.questions.count()
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    context = {
        'quiz': quiz,
        'score': round(score, 1),
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'user_answers': user_answers
    }
    return render(request, 'results.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def account_profile(request):
    quiz_attempts = UserAnswer.objects.filter(user=request.user)  # Assuming UserAnswer tracks quiz attempts
    return render(request, 'account/profile.html', {'quiz_attempts': quiz_attempts})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Invalid email format.')
            return render(request, 'account/signup.html')

        # Validate username uniqueness
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'account/signup.html')

        # Validate password complexity
        if len(password1) < 8:  # Check for minimum length
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'account/signup.html')

        if not re.search(r"[A-Za-z]", password1):  # Check for letters
            messages.error(request, 'Password must contain at least one letter.')
            return render(request, 'account/signup.html')

        if not re.search(r"\d", password1):  # Check for numbers
            messages.error(request, 'Password must contain at least one number.')
            return render(request, 'account/signup.html')

        if password1.isdigit():  # Check if password is purely numeric
            messages.error(request, 'Password cannot be entirely numeric.')
            return render(request, 'account/signup.html')

        # Check if passwords match
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)  # Log the user in after registration
                messages.success(request, 'Account created successfully! Redirecting to your profile...')
                return redirect('account_profile')  # Redirect to the profile page
            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'account/signup.html')

def login_view(request):
    if request.method == 'POST':
        login_param = request.POST.get('login')  # This can be username or email
        password = request.POST.get('password')
        user = authenticate(request, username=login_param, password=password)
        if user is not None:
            login(request, user)
            return redirect('account_profile')  # Redirect to profile after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'account/login.html')

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
