FROM python:3.11-slim
WORKDIR /runner
RUN pip install --no-cache-dir psycopg[binary]==3.2.1
COPY run_migrations.py /runner/run_migrations.py
COPY ../sql /runner/sql
CMD ["python","/runner/run_migrations.py"]
