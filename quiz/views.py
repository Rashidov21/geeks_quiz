import os
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import LeadRegistrationForm
from .models import Category, Lead, Question, QuizResult
from .telegram import notify_quiz_result
from .utils import VALID_ANSWER_CHOICES, is_rate_limited

ALLOWED_UPLOAD_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def _get_session_lead(request):
    lead_id = request.session.get('lead_id')
    if not lead_id:
        return None
    return Lead.objects.filter(id=lead_id).first()


def _get_lead_quiz_result(lead):
    try:
        return lead.quiz_result
    except QuizResult.DoesNotExist:
        return None


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
    lead = _get_session_lead(request)
    if lead:
        existing_result = _get_lead_quiz_result(lead)
        if existing_result:
            return redirect('result', result_id=existing_result.id)
        return redirect('categories')
    return redirect('register')


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'POST':
        if is_rate_limited(request, 'register', limit=5, period=3600):
            messages.error(request, 'Juda ko\'p urinish. 1 soatdan keyin qayta urinib ko\'ring.')
            return render(request, 'quiz/register.html', {'form': LeadRegistrationForm()})

        form = LeadRegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            lead, created = Lead.objects.get_or_create(
                phone_number=phone,
                defaults={
                    'full_name': form.cleaned_data['full_name'],
                    'age': form.cleaned_data['age'],
                },
            )

            existing_result = _get_lead_quiz_result(lead)
            if existing_result:
                messages.error(
                    request,
                    'Bu telefon raqami bilan allaqachon test topshirilgan.',
                )
                return render(request, 'quiz/register.html', {'form': form})

            if not created:
                lead.full_name = form.cleaned_data['full_name']
                lead.age = form.cleaned_data['age']
                lead.save(update_fields=['full_name', 'age'])

            request.session.cycle_key()
            request.session['lead_id'] = lead.id
            request.session['lead_name'] = lead.full_name
            messages.success(request, 'Ro\'yxatdan o\'tdingiz! Endi kategoriya tanlang.')
            return redirect('categories')
    else:
        form = LeadRegistrationForm()

    return render(request, 'quiz/register.html', {'form': form})


def category_view(request):
    lead = _get_session_lead(request)
    if not lead:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')

    existing_result = _get_lead_quiz_result(lead)
    if existing_result:
        messages.info(request, 'Siz allaqachon test topshirgansiz.')
        return redirect('result', result_id=existing_result.id)

    categories = Category.objects.all()
    return render(request, 'quiz/category.html', {'categories': categories})


@require_http_methods(['GET', 'POST'])
def quiz_view(request, category_id):
    lead = _get_session_lead(request)
    if not lead:
        messages.error(request, 'Avval ro\'yxatdan o\'ting.')
        return redirect('register')

    existing_result = _get_lead_quiz_result(lead)
    if existing_result:
        messages.info(request, 'Siz allaqachon test topshirgansiz.')
        return redirect('result', result_id=existing_result.id)

    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)

    if not questions.exists():
        messages.error(request, 'Bu kategoriya uchun savollar topilmadi.')
        return redirect('categories')

    if request.method == 'POST':
        if is_rate_limited(request, 'quiz_submit', limit=3, period=3600):
            messages.error(request, 'Juda ko\'p urinish. Keyinroq qayta urinib ko\'ring.')
            return redirect('categories')

        correct_count = 0
        result_data = []

        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}', '').strip().upper()
            if user_answer and user_answer not in VALID_ANSWER_CHOICES:
                user_answer = ''

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

        try:
            with transaction.atomic():
                quiz_result = QuizResult.objects.create(
                    lead=lead,
                    category=category,
                    score=score_percentage,
                    correct_answers=correct_count,
                    total_questions=total_questions,
                    result_data={'questions': result_data},
                )
        except IntegrityError:
            existing_result = _get_lead_quiz_result(lead)
            if existing_result:
                return redirect('result', result_id=existing_result.id)
            messages.error(request, 'Natija saqlanmadi. Qayta urinib ko\'ring.')
            return redirect('categories')

        notify_quiz_result(quiz_result)
        return redirect('result', result_id=quiz_result.id)

    return render(request, 'quiz/quiz.html', {
        'category': category,
        'questions': questions,
    })


def result_view(request, result_id):
    quiz_result = get_object_or_404(QuizResult, id=result_id)

    lead = _get_session_lead(request)
    if not lead or lead.id != quiz_result.lead_id:
        messages.error(request, 'Bu natijani ko\'rish huquqingiz yo\'q.')
        return redirect('register')

    return render(request, 'quiz/result.html', {
        'quiz_result': quiz_result,
        'lead': quiz_result.lead,
        'category': quiz_result.category,
        'questions_data': quiz_result.result_data.get('questions', []),
    })
