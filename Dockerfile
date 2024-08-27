# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Flask runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=server.py

# Define the command to run the Flask application
CMD ["python", "server.py"]
