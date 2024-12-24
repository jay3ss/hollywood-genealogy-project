# Use the official Python image from Docker Hub
FROM python:3.13.1-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app's directory into the container
COPY . .

# Set environment variables (you can specify these in a .env file if preferred)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run"]
