FROM python:3.6
ADD ./deploy/app /app
ADD ./contrib /app/contrib
WORKDIR /app
RUN pip install flask gunicorn pyyaml numpy matplotlib tensorflow
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app"]