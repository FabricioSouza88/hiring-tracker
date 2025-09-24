FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","-c","import time; print('Agents container ready (placeholder)'); time.sleep(3600)"]
