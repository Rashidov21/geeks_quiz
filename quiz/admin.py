from django.contrib import admin
from .models import Question, QuizResult

# Customize admin site header
admin.site.site_header = "Geeks Andijan Quiz Admin"
admin.site.site_title = "Geeks Andijan Admin"
admin.site.index_title = "Quiz Management"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'category', 'correct_option', 'id']
    list_filter = ['category']
    search_fields = ['text']
    fieldsets = (
        ('Question Details', {
            'fields': ('text', 'category')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_option')
        }),
    )


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'score', 'total_questions', 'percentage', 'date_created']
    list_filter = ['date_created']
    search_fields = ['student_name']
    readonly_fields = ['date_created', 'percentage']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'date_created')
        }),
        ('Score Details', {
            'fields': ('score', 'total_questions', 'percentage')
        }),
        ('Subject-wise Scores', {
            'fields': ('cs_score', 'html_css_score', 'js_score', 'python_score')
        }),
    )

