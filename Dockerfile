FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use fastapi command instead of uvicorn
CMD ["fastapi", "dev", "src/", "--host", "0.0.0.0", "--port", "8000"]