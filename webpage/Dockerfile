FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade Flask Werkzeug
RUN pip install "pymongo[srv]"
CMD ["python", "web/page.py"]
