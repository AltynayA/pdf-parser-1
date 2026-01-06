FROM python:3.9-slim-bullseye

# set working directory
WORKDIR /app

# install system packages for PDF -> img -> OCR pipeline
RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 

# upgrade pip -> install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install "pillow<10"
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# expose FastAPI port
EXPOSE 8000

# default command = Run FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

