# Use a slim Python image for a smaller final image size
FROM python:3.10-slim-buster

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's build cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire 'app' directory into the container's working directory
COPY ./app /app/app

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application in production using Gunicorn
# This is a robust way to run FastAPI in a production environment
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]