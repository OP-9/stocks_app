FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt waitress

COPY . .

EXPOSE 5000

# Make sure flask_file.py uses: waitress.serve(app, host='0.0.0.0', port=5000)
CMD ["python", "flask_file.py"]