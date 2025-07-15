FROM python:3.10-slim
WORKDIR /app
COPY sensor.py .
RUN pip install requests
CMD ["python", "sensor.py"]
