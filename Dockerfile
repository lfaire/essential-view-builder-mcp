FROM python:3.10-alpine3.22
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .
COPY resources/ resources/
COPY essential_viewer/ /essential_viewer/
ENV ESSENTIAL_VIEWER_DIR=/essential_viewer
CMD ["python", "server.py"]
