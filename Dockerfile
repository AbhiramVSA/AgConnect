# Use a more recent, slim Python image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's build cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local 'app' directory contents directly into the container's /app workdir
COPY ./app /app

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application in production
# The entrypoint is now just 'main:app'
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]