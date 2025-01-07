class QuizManager {
    constructor(questions, totalQuestions) {
        this.questions = questions;
        this.totalQuestions = totalQuestions;
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.userAnswers = new Array(totalQuestions).fill(null);
        
        // DOM Elements
        this.elements = {
            questionText: document.getElementById('question-text'),
            optionsList: document.getElementById('options-list'),
            backButton: document.getElementById('back-button'),
            nextButton: document.getElementById('next-button'),
            progressIndicator: document.getElementById('progress'),
            resultMessage: document.getElementById('result-message')
        };

        // Bind event listeners
        this.elements.backButton.addEventListener('click', () => this.navigate(-1));
        this.elements.nextButton.addEventListener('click', () => this.navigate(1));
        
        // Initialize the quiz
        this.updateQuestion();
    }

    updateQuestion() {
        const question = this.questions[this.currentQuestionIndex];
        
        // Update question text
        this.elements.questionText.textContent = question.text;
        
        // Clear and rebuild options list
        this.elements.optionsList.innerHTML = '';
        question.options.forEach((option, index) => {
            const li = document.createElement('li');
            li.className = 'answer-option list-group-item';
            li.textContent = option;
            li.dataset.index = index;
            
            // If this question was already answered, show the result
            if (this.userAnswers[this.currentQuestionIndex] !== null) {
                if (option === question.correct_answer) {
                    li.classList.add('correct');
                } else if (option === this.userAnswers[this.currentQuestionIndex]) {
                    li.classList.add('incorrect');
                }
                li.classList.add('disabled');
            } else {
                li.addEventListener('click', (e) => this.selectOption(e.target, question.correct_answer));
            }
            
            this.elements.optionsList.appendChild(li);
        });

        // Update progress indicator
        this.elements.progressIndicator.textContent = `${this.currentQuestionIndex + 1} of ${this.totalQuestions}`;
        
        // Update navigation buttons
        this.elements.backButton.disabled = this.currentQuestionIndex === 0;
        this.elements.nextButton.disabled = this.currentQuestionIndex === this.totalQuestions - 1 && 
                                          this.userAnswers[this.currentQuestionIndex] === null;
    }

    selectOption(selectedElement, correctAnswer) {
        const selectedText = selectedElement.textContent;
        const isCorrect = selectedText === correctAnswer;
        
        // Store the user's answer
        this.userAnswers[this.currentQuestionIndex] = selectedText;
        
        // Update score
        if (isCorrect) this.score++;
        
        // Update UI
        const options = this.elements.optionsList.getElementsByClassName('answer-option');
        Array.from(options).forEach(option => {
            option.classList.add('disabled');
            if (option.textContent === correctAnswer) {
                option.classList.add('correct');
            } else if (option === selectedElement) {
                !isCorrect && option.classList.add('incorrect');
            }
        });

        // Show result message
        this.elements.resultMessage.textContent = isCorrect ? 
            'Correct! 🎉' : 
            `Wrong! ❌ The correct answer is: ${correctAnswer}`;
        this.elements.resultMessage.className = `result-message ${isCorrect ? 'correct' : 'incorrect'}`;
        
        // Enable next button if not last question
        if (this.currentQuestionIndex < this.totalQuestions - 1) {
            this.elements.nextButton.disabled = false;
        } else {
            this.showFinalResults();
        }
    }

    navigate(direction) {
        const newIndex = this.currentQuestionIndex + direction;
        
        if (newIndex >= 0 && newIndex < this.totalQuestions) {
            this.currentQuestionIndex = newIndex;
            this.updateQuestion();
            this.elements.resultMessage.textContent = '';
        }
    }

    showFinalResults() {
        const percentage = (this.score / this.totalQuestions) * 100;
        const message = `Quiz completed! You got ${this.score} out of ${this.totalQuestions} questions correct (${percentage.toFixed(1)}%)`;
        
        // Create results summary
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'results-summary p-4 mt-4 bg-white rounded shadow';
        resultsContainer.innerHTML = `
            <h3 class="mb-3">Quiz Results</h3>
            <p class="mb-4">${message}</p>
            <div class="d-grid gap-2">
                <button onclick="location.reload()" class="btn btn-primary">Try Again</button>
                <a href="/quizzes" class="btn btn-outline-secondary">Back to Quizzes</a>
            </div>
        `;
        
        // Replace quiz content with results
        const quizContainer = document.querySelector('.quiz-container');
        quizContainer.innerHTML = '';
        quizContainer.appendChild(resultsContainer);
    }
}

// Initialize quiz when document is ready
document.addEventListener('DOMContentLoaded', () => {
    const quizManager = new QuizManager(questionsQuiz, totalQuestions);
});


//Added js template for handling quiz dunctionality//
document.addEventListener('DOMContentLoaded', function() {
    let currentQuestionIndex = 0;
    const answers = {};
    
    const questionContainer = document.getElementById('question-container');
    const questionText = document.getElementById('question-text');
    const optionsList = document.getElementById('options-list');
    const backButton = document.getElementById('back-button');
    const nextButton = document.getElementById('next-button');
    const progressIndicator = document.getElementById('progress');
    const resultMessage = document.getElementById('result-message');
    
    function updateQuestion() {
        const question = questionsQuiz[currentQuestionIndex];
        questionText.textContent = question.text;
        
        // Clear and update options
        optionsList.innerHTML = '';
        question.options.forEach((option, index) => {
            const li = document.createElement('li');
            li.className = 'list-group-item answer-option';
            li.textContent = option.text;
            li.dataset.optionId = option.id;
            
            // If this option was previously selected, highlight it
            if (answers[question.id] === option.id) {
                li.classList.add('selected');
            }
            
            li.addEventListener('click', function() {
                // Remove selection from other options
                optionsList.querySelectorAll('.answer-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                
                // Add selection to clicked option
                li.classList.add('selected');
                answers[question.id] = option.id;
            });
            
            optionsList.appendChild(li);
        });
        
        // Update navigation buttons and progress
        backButton.disabled = currentQuestionIndex === 0;
        nextButton.textContent = currentQuestionIndex === questionsQuiz.length - 1 ? 'Submit' : 'Next';
        progressIndicator.textContent = `${currentQuestionIndex + 1} of ${totalQuestions}`;
    }
    
    backButton.addEventListener('click', function() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            updateQuestion();
        }
    });
    
    nextButton.addEventListener('click', async function() {
        // Check if an option is selected
        if (!answers[questionsQuiz[currentQuestionIndex].id]) {
            resultMessage.textContent = 'Please select an answer before continuing';
            resultMessage.className = 'result-message alert alert-warning';
            return;
        }
        
        if (currentQuestionIndex < questionsQuiz.length - 1) {
            // Move to next question
            currentQuestionIndex++;
            updateQuestion();
            resultMessage.textContent = '';
        } else {
            // Submit quiz
            try {
                const response = await fetch(window.location.pathname + 'submit/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        answers: answers
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    throw new Error(data.error || 'Failed to submit quiz');
                }
            } catch (error) {
                resultMessage.textContent = error.message;
                resultMessage.className = 'result-message alert alert-danger';
            }
        }
    });
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Initialize first question
    updateQuestion();
});