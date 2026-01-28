FROM python:3.11-slim



WORKDIR /app



RUN apt-get update && apt-get install -y \

    gcc \

    default-libmysqlclient-dev \

    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt .



RUN pip install --upgrade pip && \

    pip install --no-cache-dir -r requirements.txt



COPY app.py .



EXPOSE 7000



CMD ["python", "app.py"]
