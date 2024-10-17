# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the code into the container at /app
COPY . .

# Set environment variables to prevent Python from buffering stdout and to ensure the container doesn't write pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port 8000 for the Django server
EXPOSE 8000

# Command to run the application using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "financial_backend.wsgi:application"]
