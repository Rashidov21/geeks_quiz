# Geeks Andijan — Online Quiz Application

A full-stack Django web application for online quiz testing. Students can take a 20-question quiz covering Computer Science Basics, HTML & CSS, JavaScript Basics, and Python Basics.

## Features

- 🎯 20-question quiz with 4 categories (5 questions each)
- 📊 Real-time progress tracking
- 📈 Subject-wise performance analysis
- 💾 Results stored in database
- 👨‍💼 Admin panel for managing questions and viewing results
- 📱 Responsive design for mobile and desktop
- 🎨 Clean, modern UI

## Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd geeks_quiz
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 7. Load sample questions

```bash
python manage.py load_sample_questions
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

You can:
- Add, edit, and delete questions
- View all quiz results
- See student scores and subject-wise breakdowns

## Project Structure

```
geeks_quiz/
├── manage.py
├── requirements.txt
├── quiz_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── quiz/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/quiz/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── quiz.html
│   │   └── result.html
│   ├── static/quiz/
│   │   └── style.css
│   └── management/commands/
│       └── load_sample_questions.py
└── README.md
```

## Deployment

### For Render / Railway / PythonAnywhere

1. **Update settings.py** for production:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set up PostgreSQL database (if using)

2. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Set environment variables**:
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: Set to `False` for production
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (if using PostgreSQL)

4. **Create Procfile** (for Render/Railway):
   ```
   web: gunicorn quiz_project.wsgi:application
   ```

5. **Update requirements.txt** to include:
   ```
   gunicorn
   ```

## Usage

1. **Students**: Visit the home page, enter your name, and click "Start Quiz"
2. **Teachers/Admins**: Log into the admin panel to manage questions and view results

## Quiz Categories

- **CS**: Computer Science Basics (5 questions)
- **HTML_CSS**: HTML & CSS (5 questions)
- **JS**: JavaScript Basics (5 questions)
- **PYTHON**: Python Basics (5 questions)

## License

© 2025 Geeks Andijan | Fullstack Python Entrance Test

