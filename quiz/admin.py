from django.contrib import admin
from .models import Question, QuizResult, Lead, Category

# Customize admin site header
admin.site.site_header = "Geeks Andijan Quiz Admin"
admin.site.site_title = "Geeks Andijan Admin"
admin.site.index_title = "Quiz Management"


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'age', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'phone_number']
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'category', 'correct_option', 'id']
    list_filter = ['category']
    search_fields = ['text']
    fieldsets = (
        ('Question Details', {
            'fields': ('category', 'text')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_option')
        }),
    )


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['lead', 'category', 'score', 'correct_answers', 'total_questions', 'date_taken']
    list_filter = ['date_taken', 'category']
    search_fields = ['lead__full_name']
    readonly_fields = ['date_taken']
    
    fieldsets = (
        ('Lead Information', {
            'fields': ('lead', 'category', 'date_taken')
        }),
        ('Score Details', {
            'fields': ('score', 'correct_answers', 'total_questions')
        }),
        ('Result Data', {
            'fields': ('result_data',),
            'classes': ('collapse',)
        }),
    )
