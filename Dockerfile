#
# Adapted from https://github.com/bmaingret/coach-planner/blob/main/docker/Dockerfile
#

ARG APP_NAME=brewblog
ARG APP_PATH=/$APP_NAME
ARG PYTHON_VERSION=3.12

#
# Stage: base
#
FROM python:$PYTHON_VERSION as base
ARG APP_NAME
ARG APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Copy project files
COPY . .

#
# Stage: development
#
FROM base as development
ARG APP_NAME
ARG APP_PATH

# In development mode we use the default flask webserver
ENV FLASK_APP=$APP_NAME \
    FLASK_ENV=development \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

ENTRYPOINT ["flask", "run"]

#
# Stage: production
#
FROM base as production
ARG APP_NAME
ARG APP_PATH

ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get install -y netcat-openbsd

# gunicorn port. Naming is consistent with GCP Cloud Run
ENV PORT=8888
# export APP_NAME as environment variable for the CMD
ENV APP_NAME=$APP_NAME

# Entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind :$PORT", "--workers 1", "--threads 1", "--timeout 0", "\"$APP_NAME:create_app()\""]