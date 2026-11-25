# School task manager

Django app from the Web Development course. Admins create tasks and assign them to
teachers. Teachers see their tasks on a dashboard and mark them as done.

- separate admin and teacher dashboards after login
- tasks have a priority and can be filtered
- a teacher profile is created automatically on sign-up (Django signals)

## Running

```
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The secret key and debug flag are read from `DJANGO_SECRET_KEY` / `DJANGO_DEBUG` if set.

Team project with [Seif Wael](https://github.com/Seiffwaell) and [Mohamed Waleed](https://github.com/MrWeza).
