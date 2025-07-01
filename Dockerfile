# Use the official lightweight Python image.
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME  /application
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update \
    && apt-get install -y pkg-config libmariadb-dev-compat build-essential \
    && pip install gunicorn
    
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
#EXPOSE 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
#CMD exec gunicorn --bind :8501 --workers 1 --threads 8 --timeout 0 "app:application"