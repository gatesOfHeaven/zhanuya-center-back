FROM python:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG C.UTF-8

WORKDIR /back
COPY back/requirements.txt /back/
RUN pip install --no-cache-dir -r requirements.txt
COPY back/ /back/

EXPOSE 2222
CMD ["python", "main.py"]