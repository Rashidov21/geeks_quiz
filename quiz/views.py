from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Question, QuizResult
import random


def home_view(request):
    """Home page with start quiz button"""
    return render(request, 'quiz/index.html')


def quiz_view(request):
    """Display quiz questions"""
    if request.method == 'POST':
        # Get student name from the form
        student_name = request.POST.get('student_name', '').strip()
        if not student_name:
            messages.error(request, 'Please enter your name to start the quiz.')
            return redirect('home')
        
        # Store student name in session
        request.session['student_name'] = student_name
        request.session['answers'] = {}
        request.session['current_question'] = 0
        
        # Get 20 random questions (5 from each category)
        questions = []
        for category in ['CS', 'HTML_CSS', 'JS', 'PYTHON']:
            category_questions = list(Question.objects.filter(category=category))
            if len(category_questions) >= 5:
                questions.extend(random.sample(category_questions, 5))
            else:
                questions.extend(category_questions)
        
        # If we don't have enough questions, fill with random ones
        if len(questions) < 20:
            remaining = 20 - len(questions)
            all_questions = list(Question.objects.exclude(id__in=[q.id for q in questions]))
            if len(all_questions) >= remaining:
                questions.extend(random.sample(all_questions, remaining))
            else:
                questions.extend(all_questions)
        
        # Shuffle questions
        random.shuffle(questions)
        
        # Store question IDs in session
        request.session['question_ids'] = [q.id for q in questions]
        request.session['start_time'] = timezone.now().isoformat()
        
        # Redirect to first question
        return redirect('quiz_question', question_num=1)
    
    # If not POST, redirect to home
    return redirect('home')


def quiz_question_view(request, question_num):
    """Display individual question"""
    question_ids = request.session.get('question_ids', [])
    
    if not question_ids:
        messages.error(request, 'Please start the quiz from the home page.')
        return redirect('home')
    
    if question_num < 1 or question_num > len(question_ids):
        messages.error(request, 'Invalid question number.')
        return redirect('home')
    
    # Get current question
    question_id = question_ids[question_num - 1]
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        messages.error(request, 'Question not found.')
        return redirect('home')
    
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
            messages.error(request, 'Invalid question number.')
            return redirect('home')
        
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
    
    return redirect('home')


def submit_quiz_view(request):
    """Calculate score and display results"""
    question_ids = request.session.get('question_ids', [])
    answers = request.session.get('answers', {})
    student_name = request.session.get('student_name', 'Anonymous')
    
    if not question_ids:
        messages.error(request, 'No quiz data found.')
        return redirect('home')
    
    # Calculate score
    correct_count = 0
    cs_correct = 0
    html_css_correct = 0
    js_correct = 0
    python_correct = 0
    
    for q_id in question_ids:
        question = Question.objects.get(id=q_id)
        user_answer = answers.get(str(q_id), '')
        
        if user_answer == question.correct_option:
            correct_count += 1
            # Count by category
            if question.category == 'CS':
                cs_correct += 1
            elif question.category == 'HTML_CSS':
                html_css_correct += 1
            elif question.category == 'JS':
                js_correct += 1
            elif question.category == 'PYTHON':
                python_correct += 1
    
    total_questions = len(question_ids)
    percentage = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
    
    # Save result to database
    quiz_result = QuizResult.objects.create(
        student_name=student_name,
        score=correct_count,
        total_questions=total_questions,
        cs_score=cs_correct,
        html_css_score=html_css_correct,
        js_score=js_correct,
        python_score=python_correct,
    )
    
    # Generate subject-wise feedback
    feedback = []
    categories_total = {'CS': 0, 'HTML_CSS': 0, 'JS': 0, 'PYTHON': 0}
    for q_id in question_ids:
        question = Question.objects.get(id=q_id)
        categories_total[question.category] = categories_total.get(question.category, 0) + 1
    
    # Calculate percentages for each category
    category_scores = {
        'CS': {
            'correct': cs_correct, 
            'total': categories_total.get('CS', 0),
            'percentage': round((cs_correct / categories_total.get('CS', 1)) * 100, 1) if categories_total.get('CS', 0) > 0 else 0
        },
        'HTML_CSS': {
            'correct': html_css_correct, 
            'total': categories_total.get('HTML_CSS', 0),
            'percentage': round((html_css_correct / categories_total.get('HTML_CSS', 1)) * 100, 1) if categories_total.get('HTML_CSS', 0) > 0 else 0
        },
        'JS': {
            'correct': js_correct, 
            'total': categories_total.get('JS', 0),
            'percentage': round((js_correct / categories_total.get('JS', 1)) * 100, 1) if categories_total.get('JS', 0) > 0 else 0
        },
        'PYTHON': {
            'correct': python_correct, 
            'total': categories_total.get('PYTHON', 0),
            'percentage': round((python_correct / categories_total.get('PYTHON', 1)) * 100, 1) if categories_total.get('PYTHON', 0) > 0 else 0
        },
    }
    
    for cat, data in category_scores.items():
        if data['total'] > 0:
            cat_percentage = round((data['correct'] / data['total']) * 100, 1)
            if cat_percentage >= 80:
                feedback.append(f"Excellent in {cat.replace('_', ' & ')} ({cat_percentage}%)")
            elif cat_percentage >= 60:
                feedback.append(f"Good in {cat.replace('_', ' & ')} ({cat_percentage}%)")
            else:
                feedback.append(f"Needs improvement in {cat.replace('_', ' & ')} ({cat_percentage}%)")
    
    # Clear session
    request.session.pop('question_ids', None)
    request.session.pop('answers', None)
    request.session.pop('student_name', None)
    request.session.pop('start_time', None)
    
    context = {
        'student_name': student_name,
        'score': correct_count,
        'total_questions': total_questions,
        'percentage': percentage,
        'feedback': feedback,
        'category_scores': category_scores,
    }
    
    return render(request, 'quiz/result.html', context)

