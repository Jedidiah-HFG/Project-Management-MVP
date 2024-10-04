FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--browser.serverAddress", "0.0.0.0", "--browser.gatherUsageStats", "false", "--server.port", "8080"]

#gcloud builds submit --tag gcr.io/glowing-thunder-436710-p7/streamlit-app
#gcloud builds submit --tag gcr.io/extreme-braid-436615-h5/streamlit-app