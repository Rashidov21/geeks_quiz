from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Question, QuizResult, Lead, Category
from .forms import LeadRegistrationForm
import json


def home_view(request):
    """Home page - redirect to registration"""
    # Check if lead is already registered in session
    if 'lead_id' in request.session:
        return redirect('categories')
    return redirect('register')


def register_view(request):
    """Lead registration form"""
    if request.method == 'POST':
        form = LeadRegistrationForm(request.POST)
        if form.is_valid():
            lead = form.save()
            # Store lead ID in session
            request.session['lead_id'] = lead.id
            request.session['lead_name'] = lead.full_name
            messages.success(request, 'Ro\'yxatdan o\'tdingiz! Endi kategoriya tanlang.')
            return redirect('categories')
    else:
        form = LeadRegistrationForm()
    
    return render(request, 'quiz/register.html', {'form': form})


def category_view(request):
    """Category selection page"""
    # Check if lead is registered
    if 'lead_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')
    
    categories = Category.objects.all()
    return render(request, 'quiz/category.html', {'categories': categories})


def quiz_view(request, category_id):
    """Quiz page - show all questions for selected category"""
    # Check if lead is registered
    if 'lead_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')
    
    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)
    
    if not questions.exists():
        messages.error(request, 'Bu kategoriya uchun savollar topilmadi.')
        return redirect('categories')
    
    if request.method == 'POST':
        # Process quiz submission
        lead_id = request.session.get('lead_id')
        lead = get_object_or_404(Lead, id=lead_id)
        
        # Get all answers from form
        user_answers = {}
        correct_count = 0
        result_data = []
        
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}', '').strip()
            user_answers[question.id] = user_answer
            
            is_correct = user_answer == question.correct_option
            if is_correct:
                correct_count += 1
            
            # Store result data for each question
            result_data.append({
                'question_id': question.id,
                'question_text': question.text,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'option_d': question.option_d,
                'correct_option': question.correct_option,
                'user_answer': user_answer,
                'is_correct': is_correct,
            })
        
        total_questions = questions.count()
        score_percentage = round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0
        
        # Save result to database
        quiz_result = QuizResult.objects.create(
            lead=lead,
            category=category,
            score=score_percentage,
            correct_answers=correct_count,
            total_questions=total_questions,
            result_data={'questions': result_data}
        )
        
        # Redirect to result page
        return redirect('result', result_id=quiz_result.id)
    
    # GET request - show quiz form
    context = {
        'category': category,
        'questions': questions,
    }
    
    return render(request, 'quiz/quiz.html', context)


def result_view(request, result_id):
    """Result page - show detailed quiz results"""
    quiz_result = get_object_or_404(QuizResult, id=result_id)
    
    # Extract question data from JSONField
    questions_data = quiz_result.result_data.get('questions', [])
    
    context = {
        'quiz_result': quiz_result,
        'lead': quiz_result.lead,
        'category': quiz_result.category,
        'questions_data': questions_data,
    }
    
    return render(request, 'quiz/result.html', context)
