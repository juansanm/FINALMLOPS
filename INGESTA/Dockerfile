FROM python:3.10-slim
WORKDIR /app
COPY ingesta.py .
RUN pip install pandas faker
CMD ["python", "ingesta.py"]
