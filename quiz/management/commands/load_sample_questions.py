from django.core.management.base import BaseCommand
from quiz.models import Question


class Command(BaseCommand):
    help = 'Loads sample questions for the quiz'

    def handle(self, *args, **options):
        questions_data = [
            # Computer Science Basics (5 questions)
            {
                'text': 'What does CPU stand for?',
                'category': 'CS',
                'option_a': 'Central Processing Unit',
                'option_b': 'Computer Personal Unit',
                'option_c': 'Central Program Utility',
                'option_d': 'Computer Processing Utility',
                'correct_option': 'A'
            },
            {
                'text': 'What is the smallest unit of data in a computer?',
                'category': 'CS',
                'option_a': 'Byte',
                'option_b': 'Bit',
                'option_c': 'Kilobyte',
                'option_d': 'Megabyte',
                'correct_option': 'B'
            },
            {
                'text': 'What does RAM stand for?',
                'category': 'CS',
                'option_a': 'Random Access Memory',
                'option_b': 'Read Access Memory',
                'option_c': 'Random Application Memory',
                'option_d': 'Read Application Memory',
                'correct_option': 'A'
            },
            {
                'text': 'What is the binary representation of the decimal number 10?',
                'category': 'CS',
                'option_a': '1010',
                'option_b': '1001',
                'option_c': '1100',
                'option_d': '1110',
                'correct_option': 'A'
            },
            {
                'text': 'What is the time complexity of binary search?',
                'category': 'CS',
                'option_a': 'O(n)',
                'option_b': 'O(log n)',
                'option_c': 'O(n²)',
                'option_d': 'O(1)',
                'correct_option': 'B'
            },
            # HTML & CSS (5 questions)
            {
                'text': 'What does HTML stand for?',
                'category': 'HTML_CSS',
                'option_a': 'HyperText Markup Language',
                'option_b': 'High Tech Modern Language',
                'option_c': 'HyperText Machine Language',
                'option_d': 'Home Tool Markup Language',
                'correct_option': 'A'
            },
            {
                'text': 'Which HTML tag is used to create a hyperlink?',
                'category': 'HTML_CSS',
                'option_a': '<link>',
                'option_b': '<a>',
                'option_c': '<href>',
                'option_d': '<url>',
                'correct_option': 'B'
            },
            {
                'text': 'What does CSS stand for?',
                'category': 'HTML_CSS',
                'option_a': 'Computer Style Sheets',
                'option_b': 'Cascading Style Sheets',
                'option_c': 'Creative Style Sheets',
                'option_d': 'Colorful Style Sheets',
                'correct_option': 'B'
            },
            {
                'text': 'Which CSS property is used to change the text color?',
                'category': 'HTML_CSS',
                'option_a': 'font-color',
                'option_b': 'text-color',
                'option_c': 'color',
                'option_d': 'background-color',
                'correct_option': 'C'
            },
            {
                'text': 'What is the correct way to select an element with id "header" in CSS?',
                'category': 'HTML_CSS',
                'option_a': '.header',
                'option_b': '#header',
                'option_c': 'header',
                'option_d': '*header',
                'correct_option': 'B'
            },
            # JavaScript Basics (5 questions)
            {
                'text': 'Which keyword is used to declare a variable in JavaScript?',
                'category': 'JS',
                'option_a': 'var',
                'option_b': 'variable',
                'option_c': 'v',
                'option_d': 'declare',
                'correct_option': 'A'
            },
            {
                'text': 'What is the correct way to write an array in JavaScript?',
                'category': 'JS',
                'option_a': 'var colors = (1:"red", 2:"green", 3:"blue")',
                'option_b': 'var colors = ["red", "green", "blue"]',
                'option_c': 'var colors = "red", "green", "blue"',
                'option_d': 'var colors = {1:"red", 2:"green", 3:"blue"}',
                'correct_option': 'B'
            },
            {
                'text': 'Which operator is used to compare both value and type in JavaScript?',
                'category': 'JS',
                'option_a': '==',
                'option_b': '===',
                'option_c': '=',
                'option_d': '!=',
                'correct_option': 'B'
            },
            {
                'text': 'What does DOM stand for?',
                'category': 'JS',
                'option_a': 'Document Object Model',
                'option_b': 'Data Object Model',
                'option_c': 'Dynamic Object Management',
                'option_d': 'Document Oriented Model',
                'correct_option': 'A'
            },
            {
                'text': 'Which method is used to add an element to the end of an array in JavaScript?',
                'category': 'JS',
                'option_a': 'append()',
                'option_b': 'push()',
                'option_c': 'add()',
                'option_d': 'insert()',
                'correct_option': 'B'
            },
            # Python Basics (5 questions)
            {
                'text': 'Which of the following is the correct way to print "Hello World" in Python 3?',
                'category': 'PYTHON',
                'option_a': 'print "Hello World"',
                'option_b': 'print("Hello World")',
                'option_c': 'echo "Hello World"',
                'option_d': 'printf("Hello World")',
                'correct_option': 'B'
            },
            {
                'text': 'What is the correct way to create a list in Python?',
                'category': 'PYTHON',
                'option_a': 'list = (1, 2, 3)',
                'option_b': 'list = [1, 2, 3]',
                'option_c': 'list = {1, 2, 3}',
                'option_d': 'list = <1, 2, 3>',
                'correct_option': 'B'
            },
            {
                'text': 'Which keyword is used to define a function in Python?',
                'category': 'PYTHON',
                'option_a': 'function',
                'option_b': 'def',
                'option_c': 'func',
                'option_d': 'define',
                'correct_option': 'B'
            },
            {
                'text': 'What is the output of: print(2 ** 3)',
                'category': 'PYTHON',
                'option_a': '6',
                'option_b': '8',
                'option_c': '9',
                'option_d': '5',
                'correct_option': 'B'
            },
            {
                'text': 'Which method is used to get the length of a list in Python?',
                'category': 'PYTHON',
                'option_a': 'length()',
                'option_b': 'len()',
                'option_c': 'size()',
                'option_d': 'count()',
                'correct_option': 'B'
            },
        ]

        # Clear existing questions (optional - comment out if you want to keep existing)
        # Question.objects.all().delete()

        created_count = 0
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                text=q_data['text'],
                defaults=q_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {created_count} new questions. '
                f'Total questions in database: {Question.objects.count()}'
            )
        )

