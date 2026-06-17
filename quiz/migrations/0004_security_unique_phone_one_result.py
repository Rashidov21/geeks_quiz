# Generated migration — duplicate ma'lumotlarni tozalash va unique cheklovlar

import re

from django.db import migrations, models
import django.db.models.deletion


def normalize_phone(phone):
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


def dedupe_before_constraints(apps, schema_editor):
    Lead = apps.get_model('quiz', 'Lead')
    QuizResult = apps.get_model('quiz', 'QuizResult')

    for lead in Lead.objects.all():
        normalized = normalize_phone(lead.phone_number)
        if lead.phone_number != normalized:
            lead.phone_number = normalized
            lead.save(update_fields=['phone_number'])

    seen_phones = {}
    for lead in Lead.objects.order_by('created_at', 'id'):
        if lead.phone_number in seen_phones:
            keeper = seen_phones[lead.phone_number]
            QuizResult.objects.filter(lead_id=lead.id).update(lead_id=keeper.id)
            lead.delete()
        else:
            seen_phones[lead.phone_number] = lead

    for lead in Lead.objects.all():
        results = list(
            QuizResult.objects.filter(lead_id=lead.id).order_by('date_taken', 'id')
        )
        if len(results) > 1:
            keep_id = results[0].id
            QuizResult.objects.filter(lead_id=lead.id).exclude(id=keep_id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_question_text'),
    ]

    operations = [
        migrations.RunPython(dedupe_before_constraints, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(db_index=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='lead',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='quiz_result',
                to='quiz.lead',
            ),
        ),
    ]
