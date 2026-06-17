import re

from django.core.cache import cache


def normalize_phone_number(phone):
    """Telefon raqamini yagona formatga keltiradi (+998XXXXXXXXX)."""
    if not phone:
        return phone
    digits = re.sub(r'\D', '', phone.strip())
    if len(digits) == 9:
        return f'+998{digits}'
    if digits.startswith('998') and len(digits) == 12:
        return f'+{digits}'
    if digits:
        return f'+{digits}'
    return phone.strip()


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def is_rate_limited(request, action, limit=10, period=3600):
    """So'rovlar sonini IP bo'yicha cheklaydi. True = limit oshdi."""
    ip = get_client_ip(request)
    cache_key = f'rate_limit:{action}:{ip}'
    count = cache.get(cache_key, 0)
    if count >= limit:
        return True
    cache.set(cache_key, count + 1, period)
    return False


VALID_ANSWER_CHOICES = frozenset({'A', 'B', 'C', 'D'})
