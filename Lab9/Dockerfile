FROM python:3.11-slim
WORKDIR /app
COPY *.py ./
COPY tests/ ./tests/
COPY inventory.json products.csv ./
CMD ["python", "main.py"]
