FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY app ./app
COPY faqs.csv ./
COPY embeddings_create.py ./

# optional: precompute embeddings at build time to speed first run (careful with image size)
# RUN python embeddings_create.py

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
