#!/bin/bash
# Wait for database to be ready (for SQLite, this is instant)
python manage.py migrate

# Create admin user if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@bitbox.com', '$ADMIN_PASSWORD')
    print('Admin user created successfully')
else:
    print('Admin user already exists')
"

# Start the application
gunicorn bitbox_project.wsgi:application --bind 0.0.0.0:$PORT