FROM python:3.6
ADD flask_app /app
WORKDIR /app
RUN pip install flask gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app"]