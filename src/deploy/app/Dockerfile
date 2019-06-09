FROM python:3.6
ADD ./deploy/app /app
WORKDIR /app
RUN pip install flask gunicorn pyyaml
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app"]