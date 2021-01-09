web: gunicorn docviz_app.wsgi -w 2 --bind :8000 --timeout 120
worker: python3 worker.py