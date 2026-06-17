import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

TELEGRAM_MAX_MESSAGE_LENGTH = 4096
TELEGRAM_RATE_LIMIT_SECONDS = 60


def _escape_html(text):
    if not text:
        return ''
    return (
        str(text)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
    )


def send_telegram_message(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        return False

    if len(text) > TELEGRAM_MAX_MESSAGE_LENGTH:
        text = text[: TELEGRAM_MAX_MESSAGE_LENGTH - 3] + '...'

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = json.dumps({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }).encode('utf-8')

    request = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status == 200
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            logger.warning('Telegram rate limit (429) — xabar o\'tkazib yuborildi.')
        else:
            logger.error('Telegram xabar yuborishda xato: %s', exc)
        return False
    except urllib.error.URLError as exc:
        logger.error('Telegram xabar yuborishda xato: %s', exc)
        return False


def format_quiz_result_message(quiz_result):
    lead = quiz_result.lead
    category = quiz_result.category
    questions = quiz_result.result_data.get('questions', [])

    lines = [
        '🆕 <b>Yangi test natijasi</b>',
        '',
        f'👤 <b>Ism:</b> {_escape_html(lead.full_name)}',
        f'📞 <b>Telefon:</b> {_escape_html(lead.phone_number)}',
        f'🎂 <b>Yosh:</b> {lead.age}',
        f'📚 <b>Yo\'nalish:</b> {_escape_html(category.name)}',
        '',
        f'📊 <b>Ball:</b> {quiz_result.score}%',
        f'✅ <b>To\'g\'ri:</b> {quiz_result.correct_answers} / {quiz_result.total_questions}',
        '',
        '<b>Savollar bo\'yicha:</b>',
    ]

    for index, item in enumerate(questions, start=1):
        status = '✅' if item.get('is_correct') else '❌'
        question_text = strip_tags(item.get('question_text', '')).strip()
        if len(question_text) > 100:
            question_text = question_text[:100] + '...'
        user_answer = item.get('user_answer') or '—'
        lines.append(
            f'{index}. {status} {_escape_html(question_text)} '
            f'(Javob: {user_answer})'
        )

    return '\n'.join(lines)


def notify_quiz_result(quiz_result):
    """Har bir telefon uchun Telegram xabarini cheklaydi."""
    phone = quiz_result.lead.phone_number
    cache_key = f'telegram_sent:{phone}'
    if cache.get(cache_key):
        return False

    message = format_quiz_result_message(quiz_result)
    sent = send_telegram_message(message)
    if sent:
        cache.set(cache_key, True, TELEGRAM_RATE_LIMIT_SECONDS)
    return sent
