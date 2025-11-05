from django.db import models


class Question(models.Model):
    CATEGORY_CHOICES = [
        ('CS', 'Computer Science Basics'),
        ('HTML_CSS', 'HTML & CSS'),
        ('JS', 'JavaScript Basics'),
        ('PYTHON', 'Python Basics'),
    ]
    
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ])
    
    class Meta:
        ordering = ['category', 'id']
    
    def __str__(self):
        return f"{self.category} - {self.text[:50]}..."


class QuizResult(models.Model):
    student_name = models.CharField(max_length=100)
    score = models.IntegerField()
    total_questions = models.IntegerField(default=20)
    date_created = models.DateTimeField(auto_now_add=True)
    
    # Store subject-wise scores for feedback
    cs_score = models.IntegerField(default=0)
    html_css_score = models.IntegerField(default=0)
    js_score = models.IntegerField(default=0)
    python_score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.student_name} - {self.score}%"
    
    @property
    def percentage(self):
        """Calculate percentage score"""
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 1)

