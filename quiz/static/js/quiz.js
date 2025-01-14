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
        const answers = {};
        
        // Prepare answers data
        this.userAnswers.forEach((answer, index) => {
            if (answer !== null) {
                answers[this.questions[index].id] = answer;
            }
        });
        
        // Submit answers to server
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json'
            },
            body: JSON.stringify({ answers: answers })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                throw new Error(data.error || 'Failed to submit quiz');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to submit quiz. Please try again.');
        });
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialize quiz when document is ready
document.addEventListener('DOMContentLoaded', () => {
    const quizManager = new QuizManager(questionsQuiz, totalQuestions);
});