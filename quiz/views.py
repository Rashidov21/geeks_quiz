import os
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LeadRegistrationForm
from .models import Category, Lead, Question, QuizResult
from .telegram import notify_quiz_result

ALLOWED_UPLOAD_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


@staff_member_required
@require_POST
def custom_upload_function(request):
    """CKEditor admin panel orqali rasm yuklash (faqat staff uchun)."""
    upload = request.FILES.get('upload')

    if not upload:
        return JsonResponse({'error': 'Fayl topilmadi!'}, status=400)

    if upload.size > MAX_UPLOAD_SIZE:
        return JsonResponse({'error': 'Fayl hajmi 5MB dan oshmasligi kerak.'}, status=400)

    ext = os.path.splitext(upload.name)[1].lower()
    if ext not in ALLOWED_UPLOAD_EXTENSIONS:
        return JsonResponse({'error': 'Faqat rasm fayllari ruxsat etilgan.'}, status=400)

    safe_name = f'{uuid.uuid4().hex}{ext}'
    file_path = default_storage.save(os.path.join('uploads', safe_name), upload)
    file_url = settings.MEDIA_URL + file_path

    return JsonResponse({'url': file_url})


def home_view(request):
    """Home page - redirect to registration"""
    if 'lead_id' in request.session:
        return redirect('categories')
    return redirect('register')


def register_view(request):
    """Lead registration form"""
    if request.method == 'POST':
        form = LeadRegistrationForm(request.POST)
        if form.is_valid():
            lead = form.save()
            request.session['lead_id'] = lead.id
            request.session['lead_name'] = lead.full_name
            messages.success(request, 'Ro\'yxatdan o\'tdingiz! Endi kategoriya tanlang.')
            return redirect('categories')
    else:
        form = LeadRegistrationForm()

    return render(request, 'quiz/register.html', {'form': form})


def category_view(request):
    """Category selection page"""
    if 'lead_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')

    categories = Category.objects.all()
    return render(request, 'quiz/category.html', {'categories': categories})


def quiz_view(request, category_id):
    """Quiz page - show all questions for selected category"""
    if 'lead_id' not in request.session:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')

    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)

    if not questions.exists():
        messages.error(request, 'Bu kategoriya uchun savollar topilmadi.')
        return redirect('categories')

    if request.method == 'POST':
        lead_id = request.session.get('lead_id')
        lead = get_object_or_404(Lead, id=lead_id)

        correct_count = 0
        result_data = []

        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}', '').strip()

            is_correct = user_answer == question.correct_option
            if is_correct:
                correct_count += 1

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

        quiz_result = QuizResult.objects.create(
            lead=lead,
            category=category,
            score=score_percentage,
            correct_answers=correct_count,
            total_questions=total_questions,
            result_data={'questions': result_data}
        )

        notify_quiz_result(quiz_result)

        return redirect('result', result_id=quiz_result.id)

    context = {
        'category': category,
        'questions': questions,
    }

    return render(request, 'quiz/quiz.html', context)


def result_view(request, result_id):
    """Result page - show detailed quiz results"""
    quiz_result = get_object_or_404(QuizResult, id=result_id)

    lead_id = request.session.get('lead_id')
    if lead_id != quiz_result.lead_id:
        messages.error(request, 'Bu natijani ko\'rish huquqingiz yo\'q.')
        return redirect('register')

    questions_data = quiz_result.result_data.get('questions', [])

    context = {
        'quiz_result': quiz_result,
        'lead': quiz_result.lead,
        'category': quiz_result.category,
        'questions_data': questions_data,
    }

    return render(request, 'quiz/result.html', context)
