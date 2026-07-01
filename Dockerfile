FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt
COPY monitor.py auth.py get_chats.py send_test.py ./
CMD ["python", "monitor.py"]