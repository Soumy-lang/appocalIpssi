# Use the official lightweight Python image.
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /application
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --upgrade pip \
    && pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Streamlit application
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=172.19.0.2"]
