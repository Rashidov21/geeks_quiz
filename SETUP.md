# Quick Setup Guide

## Initial Setup (First Time)

1. **Install Python** (3.8 or higher)

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Load sample questions:**
   ```bash
   python manage.py load_sample_questions
   ```

7. **Start the server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Home page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Daily Usage

1. Activate virtual environment
2. Run `python manage.py runserver`
3. Visit http://127.0.0.1:8000/

## Adding More Questions

You can add questions through:
1. **Admin Panel** (recommended): http://127.0.0.1:8000/admin/quiz/question/
2. **Management command**: Modify `quiz/management/commands/load_sample_questions.py` and run it again

## Troubleshooting

### Database Issues
- Delete `db.sqlite3` and run `python manage.py migrate` again

### Static Files Not Loading
- Run `python manage.py collectstatic` (for production)

### Questions Not Appearing
- Make sure you've run `python manage.py load_sample_questions`
- Check admin panel to verify questions exist

