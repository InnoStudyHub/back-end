FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /studyhub
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN echo ${GC_KEY} > google_cloud_key.json