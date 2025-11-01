FROM python:3.10-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r app/requirements.txt
COPY app ./app
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./dev.db
ENV UPLOAD_DIR=/tmp/tandemhire_uploads
RUN mkdir -p /tmp/tandemhire_uploads
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
