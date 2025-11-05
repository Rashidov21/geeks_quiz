from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Question, QuizResult, Student
from .forms import StudentRegistrationForm
import random


def home_view(request):
    """Home page - redirect to registration"""
    # Check if student is already registered in session
    if 'student_id' in request.session:
        return redirect('category_selection')
    return redirect('register')


def register_view(request):
    """Student registration form"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Store student ID in session
            request.session['student_id'] = student.id
            request.session['student_name'] = student.full_name
            messages.success(request, 'Ro\'yxatdan o\'tdingiz! Endi kategoriya tanlang.')
            return redirect('category_selection')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'quiz/register.html', {'form': form})


def category_selection_view(request):
    """Category selection page"""
    # Check if student is registered
    if 'student_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')
    
    return render(request, 'quiz/category.html')


def quiz_view(request):
    """Start quiz with selected category"""
    # Check if student is registered
    if 'student_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')
    
    if request.method == 'POST':
        # Get selected category
        category = request.POST.get('category', '').strip()
        
        if category not in ['CS', 'HTML_CSS', 'JS', 'PYTHON']:
            messages.error(request, 'Noto\'g\'ri kategoriya tanlandi.')
            return redirect('category_selection')
        
        # Store category in session
        request.session['selected_category'] = category
        request.session['answers'] = {}
        
        # Get questions from selected category (5 questions)
        category_questions = list(Question.objects.filter(category=category))
        
        if len(category_questions) >= 5:
            questions = random.sample(category_questions, 5)
        else:
            questions = category_questions
        
        # Shuffle questions
        random.shuffle(questions)
        
        # Store question IDs in session
        request.session['question_ids'] = [q.id for q in questions]
        request.session['start_time'] = timezone.now().isoformat()
        
        # Redirect to first question
        return redirect('quiz_question', question_num=1)
    
    # If not POST, redirect to category selection
    return redirect('category_selection')


def quiz_question_view(request, question_num):
    """Display individual question"""
    # Check if student is registered and quiz started
    if 'student_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')
    
    question_ids = request.session.get('question_ids', [])
    
    if not question_ids:
        messages.error(request, 'Kategoriya tanlang va quizni boshlang.')
        return redirect('category_selection')
    
    if question_num < 1 or question_num > len(question_ids):
        messages.error(request, 'Noto\'g\'ri savol raqami.')
        return redirect('category_selection')
    
    # Get current question
    question_id = question_ids[question_num - 1]
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        messages.error(request, 'Savol topilmadi.')
        return redirect('category_selection')
    
    # Get previously selected answer if any
    answers = request.session.get('answers', {})
    selected_answer = answers.get(str(question_id), '')
    
    context = {
        'question': question,
        'question_num': question_num,
        'total_questions': len(question_ids),
        'selected_answer': selected_answer,
    }
    
    return render(request, 'quiz/quiz.html', context)


def save_answer_view(request, question_num):
    """Save answer and move to next question"""
    if request.method == 'POST':
        question_ids = request.session.get('question_ids', [])
        
        if question_num < 1 or question_num > len(question_ids):
            messages.error(request, 'Noto\'g\'ri savol raqami.')
            return redirect('category_selection')
        
        # Get selected answer
        selected_answer = request.POST.get('answer', '')
        question_id = question_ids[question_num - 1]
        
        # Save answer to session
        answers = request.session.get('answers', {})
        answers[str(question_id)] = selected_answer
        request.session['answers'] = answers
        
        # Move to next question or submit
        if question_num < len(question_ids):
            return redirect('quiz_question', question_num=question_num + 1)
        else:
            return redirect('submit_quiz')
    
    return redirect('category_selection')


def submit_quiz_view(request):
    """Calculate score and display results"""
    # Check if student is registered
    if 'student_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')
    
    question_ids = request.session.get('question_ids', [])
    answers = request.session.get('answers', {})
    student_id = request.session.get('student_id')
    student_name = request.session.get('student_name', 'Anonymous')
    selected_category = request.session.get('selected_category', '')
    
    if not question_ids:
        messages.error(request, 'Quiz ma\'lumotlari topilmadi.')
        return redirect('category_selection')
    
    # Get student object
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        student = None
    
    # Calculate score
    correct_count = 0
    
    for q_id in question_ids:
        question = Question.objects.get(id=q_id)
        user_answer = answers.get(str(q_id), '')
        
        if user_answer == question.correct_option:
            correct_count += 1
    
    total_questions = len(question_ids)
    percentage = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
    
    # Get category display name
    category_display = dict(Question.CATEGORY_CHOICES).get(selected_category, selected_category)
    
    # Generate feedback message
    if percentage >= 80:
        feedback_message = "Ajoyib! Siz Fullstack Python kursi uchun tayyorsiz!"
    else:
        feedback_message = "Yaxshi harakat! Bilimingizni biroz mustahkamlang."
    
    # Save result to database
    quiz_result = QuizResult.objects.create(
        student=student,
        student_name=student_name,
        category=selected_category,
        score=correct_count,
        total_questions=total_questions,
    )
    
    # Clear session
    request.session.pop('question_ids', None)
    request.session.pop('answers', None)
    request.session.pop('selected_category', None)
    request.session.pop('start_time', None)
    # Keep student info in session so they can take another quiz
    
    context = {
        'student': student,
        'student_name': student_name,
        'category': category_display,
        'score': correct_count,
        'total_questions': total_questions,
        'percentage': percentage,
        'feedback_message': feedback_message,
    }
    
    return render(request, 'quiz/result.html', context)
