FROM python:3.6-alpine
WORKDIR /litourgiya
ENV PYTHONPATH /litourgiya/
ENV FLASK_APP /litourgiya/app.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./litourgiya ./
CMD python app.py
