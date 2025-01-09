FROM python:3.12.7-slim

RUN python -m pip install --upgrade pip

WORKDIR /workspace
ENV PYTHONPATH="${PYTHONPATH}:."

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/ src/